#!/usr/bin/env python3
"""Build browser-ready Allen CCF 2017 atlas assets for the stereotaxic viewer.

Input arrays are the files used by cortex-lab/allenCCF:
  template_volume_10um.npy
  annotation_volume_10um_by_index.npy
  structure_tree_safe_2017.csv

The arrays are expected in [AP, DV, ML] order. The output contains compact,
gzip-compressed binary volumes plus a manifest and structure ontology. The
web viewer loads these files only when the 2D atlas is enabled.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Any, Iterable

import numpy as np

FIGSHARE_ARTICLE_ID = 25365829
FIGSHARE_API = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"
ALLEN_DOWNLOAD_ROOT = "https://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf"
EXPECTED_SHAPES = {10: (1320, 800, 1140), 25: (528, 320, 456), 50: (264, 160, 228), 100: (132, 80, 114)}
REQUIRED_SOURCE_FILES = {
    "template_volume_10um.npy",
    "annotation_volume_10um_by_index.npy",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert the cortex-lab Allen CCF 2017 volumes into web assets."
    )
    parser.add_argument("--template", type=Path, help="Path to template_volume_10um.npy")
    parser.add_argument("--annotation", type=Path, help="Path to annotation_volume_10um_by_index.npy")
    parser.add_argument(
        "--structures",
        type=Path,
        default=Path(__file__).with_name("structure_tree_safe_2017.csv"),
        help="Path to structure_tree_safe_2017.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "atlas-data",
        help="Output atlas-data directory",
    )
    parser.add_argument(
        "--resolution-um",
        type=int,
        choices=(25, 50, 100),
        default=50,
        help="Web volume resolution. 50 µm is the recommended balance.",
    )
    parser.add_argument(
        "--source-resolution-um",
        type=int,
        choices=(10, 25, 50, 100),
        help="Resolution of manually supplied volumes. Defaults to 10 µm for NPY and to the output resolution for NRRD.",
    )
    parser.add_argument(
        "--official",
        action="store_true",
        help="Download the official Allen template and CCF 2017 annotation NRRDs at the requested resolution. Recommended.",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the two cortex-lab Figshare 10 µm NPY files before building (about 4.48 GB total).",
    )
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=Path("allen-ccf-source"),
        help="Directory used by --download",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing atlas-data directory.",
    )
    return parser.parse_args()


def human_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def progress_download(url: str, destination: Path, expected_size: int | None = None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    downloaded = partial.stat().st_size if partial.exists() else 0
    headers: dict[str, str] = {}
    if downloaded:
        headers["Range"] = f"bytes={downloaded}-"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:  # nosec B310: trusted Figshare API URLs
        status = getattr(response, "status", 200)
        if downloaded and status != 206:
            downloaded = 0
            partial.unlink(missing_ok=True)
        mode = "ab" if downloaded else "wb"
        total = expected_size or 0
        if not total:
            length = response.headers.get("Content-Length")
            if length:
                total = int(length) + downloaded
        with partial.open(mode) as handle:
            while True:
                chunk = response.read(8 * 1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(
                        f"\r  {destination.name}: {human_bytes(downloaded)} / {human_bytes(total)} ({pct:5.1f}%)",
                        end="",
                        flush=True,
                    )
                else:
                    print(
                        f"\r  {destination.name}: {human_bytes(downloaded)}",
                        end="",
                        flush=True,
                    )
    print()
    partial.replace(destination)


def download_figshare_files(download_dir: Path) -> tuple[Path, Path]:
    print(f"Querying Figshare article {FIGSHARE_ARTICLE_ID}…")
    with urllib.request.urlopen(FIGSHARE_API) as response:  # nosec B310
        metadata = json.load(response)
    files = {item["name"]: item for item in metadata.get("files", [])}
    missing = REQUIRED_SOURCE_FILES.difference(files)
    if missing:
        raise RuntimeError(f"Figshare article is missing expected files: {sorted(missing)}")

    download_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name in sorted(REQUIRED_SOURCE_FILES):
        item = files[name]
        path = download_dir / name
        size = int(item.get("size", 0)) or None
        if path.exists() and (size is None or path.stat().st_size == size):
            print(f"Using existing {path} ({human_bytes(path.stat().st_size)}).")
        else:
            print(f"Downloading {name}…")
            progress_download(item["download_url"], path, size)
        paths[name] = path
    return paths["template_volume_10um.npy"], paths["annotation_volume_10um_by_index.npy"]


def download_official_files(resolution_um: int, download_dir: Path) -> tuple[Path, Path]:
    if resolution_um not in EXPECTED_SHAPES:
        raise ValueError(f"No configured official Allen volume for {resolution_um} µm")
    download_dir.mkdir(parents=True, exist_ok=True)
    template_name = f"average_template_{resolution_um}.nrrd"
    annotation_name = f"annotation_{resolution_um}.nrrd"
    template_url = f"{ALLEN_DOWNLOAD_ROOT}/average_template/{template_name}"
    annotation_url = f"{ALLEN_DOWNLOAD_ROOT}/annotation/ccf_2017/{annotation_name}"
    template_path = download_dir / template_name
    annotation_path = download_dir / annotation_name
    for url, path in ((template_url, template_path), (annotation_url, annotation_path)):
        if path.exists() and path.stat().st_size > 0:
            print(f"Using existing {path} ({human_bytes(path.stat().st_size)}).")
        else:
            print(f"Downloading {path.name} from the Allen Institute…")
            progress_download(url, path)
    return template_path, annotation_path


def load_volume(path: Path) -> np.ndarray:
    suffix = path.suffix.lower()
    if suffix == ".npy":
        return np.load(path, mmap_mode="r", allow_pickle=False)
    if suffix == ".nrrd":
        try:
            import nrrd  # type: ignore
        except ImportError as exc:
            raise RuntimeError("Reading NRRD files requires pynrrd: pip install -r tools/requirements-atlas.txt") from exc
        data, _header = nrrd.read(str(path), index_order="C")
        return data
    raise ValueError(f"Unsupported volume format: {path}")


def orient_volume(volume: np.ndarray, resolution_um: int, label: str) -> np.ndarray:
    expected = EXPECTED_SHAPES.get(resolution_um)
    if expected is None:
        return volume

    shape = tuple(int(value) for value in volume.shape)
    if shape == expected:
        return volume

    # Official Allen NRRD files can be returned by pynrrd in a different
    # axis order from the viewer's required [AP, DV, ML] convention.
    # All configured atlas dimensions are unique, so the required
    # permutation can be identified safely from the shape.
    if sorted(shape) == sorted(expected) and len(set(expected)) == 3:
        axes = tuple(shape.index(size) for size in expected)
        print(
            f"Transposing {label} from shape {shape} to {expected} "
            f"in [AP, DV, ML] order using axes {axes}."
        )
        oriented = np.transpose(volume, axes)
        if tuple(oriented.shape) == expected:
            return oriented

    raise ValueError(
        f"{label} shape {volume.shape} does not match expected "
        f"{expected} for {resolution_um} µm"
    )


def clean_hex(value: str) -> str:
    text = (value or "FFFFFF").strip().lstrip("#").upper()
    if len(text) == 5:  # known leading-zero issue in the source table
        text = "0" + text
    if len(text) != 6 or any(char not in "0123456789ABCDEF" for char in text):
        return "FFFFFF"
    return text


def read_structures(csv_path: Path) -> tuple[list[dict[str, Any] | None], dict[int, int]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Structure tree not found: {csv_path}")
    structures: list[dict[str, Any] | None] = [None]
    id_to_value: dict[int, int] = {}
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "name", "acronym", "color_hex_triplet", "parent_structure_id"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("The structure CSV does not match structure_tree_safe_2017.csv")
        for value_index, row in enumerate(reader, start=1):
            parent = row.get("parent_structure_id", "").strip()
            structure_id = int(float(row["id"]))
            id_to_value[structure_id] = value_index
            structures.append(
                {
                    "value": value_index,
                    "id": structure_id,
                    "name": row["name"],
                    "acronym": row["acronym"],
                    "colour": f"#{clean_hex(row['color_hex_triplet'])}",
                    "parent_structure_id": int(float(parent)) if parent else None,
                    "structure_id_path": row.get("structure_id_path", ""),
                }
            )
    return structures, id_to_value


def gzip_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as archive:
            archive.write(payload)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sampled_percentiles(volume: np.ndarray, step: int) -> tuple[float, float]:
    sample_step = max(step * 4, 20)
    sample = np.asarray(volume[::sample_step, ::sample_step, ::sample_step], dtype=np.float32)
    nonzero = sample[sample > 0]
    basis = nonzero if nonzero.size else sample.reshape(-1)
    low, high = np.percentile(basis, [0.5, 99.7])
    if not np.isfinite(low) or not np.isfinite(high) or high <= low:
        low = float(np.min(basis))
        high = float(np.max(basis))
    if high <= low:
        high = low + 1.0
    return float(low), float(high)


def downsample_template(volume: np.ndarray, step: int, low: float, high: float) -> np.ndarray:
    output_shape = tuple((size + step - 1) // step for size in volume.shape)
    output = np.empty(output_shape, dtype=np.uint8)
    scale = 255.0 / (high - low)
    ap_indices = range(0, volume.shape[0], step)
    total = output_shape[0]
    for out_ap, src_ap in enumerate(ap_indices):
        plane = np.asarray(volume[src_ap, ::step, ::step], dtype=np.float32)
        plane = np.clip((plane - low) * scale, 0, 255)
        output[out_ap] = plane.astype(np.uint8)
        if out_ap % max(1, total // 20) == 0 or out_ap + 1 == total:
            print(f"\r  template: {out_ap + 1}/{total} coronal planes", end="", flush=True)
    print()
    return output


def downsample_annotation(
    volume: np.ndarray,
    step: int,
    id_to_value: dict[int, int] | None = None,
) -> np.ndarray:
    output_shape = tuple((size + step - 1) // step for size in volume.shape)
    output = np.empty(output_shape, dtype=np.uint16)
    sorted_ids: np.ndarray | None = None
    sorted_values: np.ndarray | None = None
    if id_to_value is not None:
        sorted_pairs = sorted(id_to_value.items())
        sorted_ids = np.asarray([pair[0] for pair in sorted_pairs], dtype=np.uint32)
        sorted_values = np.asarray([pair[1] for pair in sorted_pairs], dtype=np.uint16)
    ap_indices = range(0, volume.shape[0], step)
    total = output_shape[0]
    for out_ap, src_ap in enumerate(ap_indices):
        plane = np.asarray(volume[src_ap, ::step, ::step])
        if sorted_ids is None or sorted_values is None:
            if np.max(plane, initial=0) > np.iinfo(np.uint16).max:
                raise ValueError("Annotation values exceed uint16; expected cortex-lab by-index volume")
            mapped = plane.astype(np.uint16, copy=False)
        else:
            ids = plane.astype(np.uint32, copy=False)
            positions = np.searchsorted(sorted_ids, ids)
            valid = positions < sorted_ids.size
            safe_positions = np.minimum(positions, sorted_ids.size - 1)
            valid &= sorted_ids[safe_positions] == ids
            mapped = np.zeros(ids.shape, dtype=np.uint16)
            mapped[valid] = sorted_values[safe_positions[valid]]
        output[out_ap] = mapped
        if out_ap % max(1, total // 20) == 0 or out_ap + 1 == total:
            print(f"\r  annotation: {out_ap + 1}/{total} coronal planes", end="", flush=True)
    print()
    return output


def validate_source(template: np.ndarray, annotation: np.ndarray, source_resolution_um: int) -> None:
    if template.ndim != 3 or annotation.ndim != 3:
        raise ValueError("Template and annotation must both be 3D arrays")
    if template.shape != annotation.shape:
        raise ValueError(f"Volume shapes differ: template {template.shape}, annotation {annotation.shape}")
    expected = EXPECTED_SHAPES.get(source_resolution_um)
    if expected and template.shape != expected:
        print(f"Warning: source shape is {template.shape}, not expected {expected} at {source_resolution_um} µm.", file=sys.stderr)


def build(args: argparse.Namespace) -> None:
    if args.official and args.download:
        raise SystemExit("Choose either --official or --download, not both.")
    template_path = args.template
    annotation_path = args.annotation
    annotation_mode = "by-index"
    source_workflow = "cortex-lab/allenCCF by-index annotation volume"
    source_resolution_um = args.source_resolution_um or 10
    if args.official:
        template_path, annotation_path = download_official_files(args.resolution_um, args.download_dir)
        source_resolution_um = args.resolution_um
        annotation_mode = "structure-id"
        source_workflow = "Official Allen CCF 2017 template and structure-ID annotation NRRDs"
    elif args.download:
        template_path, annotation_path = download_figshare_files(args.download_dir)
    if template_path is None or annotation_path is None:
        raise SystemExit("Provide --template and --annotation, use --official, or use --download.")
    if not template_path.exists():
        raise FileNotFoundError(template_path)
    if not annotation_path.exists():
        raise FileNotFoundError(annotation_path)
    if template_path.suffix.lower() == ".nrrd" or annotation_path.suffix.lower() == ".nrrd":
        annotation_mode = "structure-id"
        source_workflow = "Allen CCF NRRD template and structure-ID annotation"
        source_resolution_um = args.source_resolution_um or args.resolution_um
    if args.resolution_um < source_resolution_um or args.resolution_um % source_resolution_um:
        raise ValueError(f"Output resolution must be an integer multiple of the {source_resolution_um} µm source resolution")
    step = args.resolution_um // source_resolution_um

    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        if not args.overwrite:
            raise FileExistsError(f"{output} is not empty. Add --overwrite to replace it.")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    print("Opening source volumes…")
    template = orient_volume(load_volume(template_path), source_resolution_um, "template")
    annotation = orient_volume(load_volume(annotation_path), source_resolution_um, "annotation")
    validate_source(template, annotation, source_resolution_um)

    structures, id_to_value = read_structures(args.structures)
    if annotation_mode == "by-index":
        max_label = int(np.max(annotation[::max(step * 4, 20), ::max(step * 4, 20), ::max(step * 4, 20)], initial=0))
        if max_label >= len(structures):
            print(f"Warning: sampled annotation value {max_label} exceeds structure table value range {len(structures)-1}.", file=sys.stderr)

    low, high = sampled_percentiles(template, step)
    print(f"Template display range: {low:.3f} to {high:.3f}")
    template_out = downsample_template(template, step, low, high)
    annotation_out = downsample_annotation(annotation, step, id_to_value if annotation_mode == "structure-id" else None)

    template_file = output / "template.uint8.gz"
    annotation_file = output / "annotation.uint16le.gz"
    structures_file = output / "structures.json"

    print("Compressing web volumes…")
    gzip_write(template_file, np.ascontiguousarray(template_out).tobytes(order="C"))
    annotation_le = np.ascontiguousarray(annotation_out.astype("<u2", copy=False))
    gzip_write(annotation_file, annotation_le.tobytes(order="C"))
    structures_file.write_text(
        json.dumps(structures, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    shape = [int(value) for value in template_out.shape]
    voxel_mm = args.resolution_um / 1000.0
    files = {
        "template": {
            "path": template_file.name,
            "dtype": "uint8",
            "compression": "gzip",
            "bytes_uncompressed": int(template_out.nbytes),
            "bytes_compressed": template_file.stat().st_size,
            "sha256": sha256(template_file),
        },
        "annotation": {
            "path": annotation_file.name,
            "dtype": "uint16le",
            "compression": "gzip",
            "bytes_uncompressed": int(annotation_out.nbytes),
            "bytes_compressed": annotation_file.stat().st_size,
            "sha256": sha256(annotation_file),
        },
        "structures": {
            "path": structures_file.name,
            "sha256": sha256(structures_file),
        },
    }
    manifest = {
        "schema_version": 1,
        "ready": True,
        "atlas": "Allen Mouse Brain Common Coordinate Framework v3",
        "annotation_release": "CCF 2017",
        "source_workflow": source_workflow,
        "source_resolution_um": source_resolution_um,
        "source_annotation_values": annotation_mode,
        "resolution_um": args.resolution_um,
        "voxel_size_mm": voxel_mm,
        "axis_order": ["AP", "DV", "ML"],
        "shape_ap_dv_ml": shape,
        "native_sections": {
            "coronal": {"width": shape[2], "height": shape[1], "slice_count": shape[0]},
            "sagittal": {"width": shape[0], "height": shape[1], "slice_count": shape[2]},
        },
        "volume_origin_mm": {"ap": 0.0, "dv": 0.0, "ml": 0.0},
        "reference_bregma_10um_voxels": {"ap": 540, "dv": 0, "ml": 570},
        "coordinate_mapping": {
            "ap_index": "round((bregma_ap_mm - AP_mm) / voxel_size_mm)",
            "dv_index": "round((bregma_dv_mm - DV_mm) / voxel_size_mm)",
            "ml_index": "round((midline_ml_mm - ML_mm) / voxel_size_mm)",
            "ml_sign": "left positive, right negative",
            "dv_sign": "ventral targets are negative in this application",
        },
        "sampling": {
            "method": ("native source resolution" if step == 1 else f"regular-grid nearest-neighbour from the {source_resolution_um} µm source"),
            "step_source_voxels": step,
            "template_normalisation_percentiles": [0.5, 99.7],
            "template_display_range": [low, high],
        },
        "files": files,
        "licence": ("Allen Institute data terms and attribution apply." if args.official else "CC BY 4.0 for the modified Figshare dataset; retain Allen Institute attribution and applicable terms."),
        "citation": {
            "figshare_doi": "10.6084/m9.figshare.25365829",
            "ccf_publication_doi": "10.1016/j.cell.2020.04.007",
            "software_repository": "cortex-lab/allenCCF",
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\nAtlas assets created:")
    print(f"  output: {output}")
    print(f"  resolution: {args.resolution_um} µm")
    print(f"  shape [AP, DV, ML]: {shape}")
    print(f"  template: {human_bytes(template_file.stat().st_size)} compressed")
    print(f"  annotation: {human_bytes(annotation_file.stat().st_size)} compressed")
    print(f"  structures: {len(structures)-1} ontology rows")
    for generated in (template_file, annotation_file):
        if generated.stat().st_size >= 95 * 1024 * 1024:
            print(f"Warning: {generated.name} is near or above GitHub's ordinary per-file limit; rebuild at 50 or 100 µm.", file=sys.stderr)


if __name__ == "__main__":
    try:
        build(parse_args())
    except KeyboardInterrupt:
        raise SystemExit("Cancelled.")
    except Exception as exc:
        raise SystemExit(f"Error: {exc}") from exc
