#!/usr/bin/env python3
"""Validate TCASIA workflow configuration before running Snakemake."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = REPOSITORY_ROOT / "workflows" / "lib"
sys.path.insert(0, str(LIB_DIR))

from tcasia_config import load_samples, normalize_strandness, require_config


REQUIRED_KEYS = {
    "alignment": ("samples", "output_dir", "star_index_DIR", "ref", "strandness"),
    "as_calling": (
        "samples",
        "output_dir",
        "bam_dir",
        "ref",
        "GFF",
        "MAJIQ_license",
        "suppa2_events",
        "SALMON_INDEX",
        "read_len",
        "strandness",
    ),
}


def resolve_path(value: str, config_path: Path) -> Path:
    """Resolve paths using the current directory, then the config directory."""
    path = Path(value).expanduser()
    if path.is_absolute():
        return path

    from_current_directory = (Path.cwd() / path).resolve()
    if from_current_directory.exists():
        return from_current_directory
    return (config_path.parent / path).resolve()


def read_config(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Configuration root must be a YAML mapping")
    return data


def check_positive_integer(config: Dict[str, Any], key: str) -> None:
    value = config.get(key)
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"Configuration key '{key}' must be a positive integer")


def validate(workflow_name: str, config_path: Path, check_files: bool) -> int:
    config = read_config(config_path)
    require_config(config, *REQUIRED_KEYS[workflow_name])
    normalize_strandness(str(config["strandness"]))

    sample_sheet = resolve_path(str(config["samples"]), config_path)
    samples = load_samples(str(sample_sheet))

    if workflow_name == "as_calling":
        check_positive_integer(config, "read_len")

    if check_files:
        missing = []
        for sample_id, record in samples.items():
            for field in ("fastq_1", "fastq_2"):
                path = resolve_path(record[field], config_path)
                if not path.is_file():
                    missing.append(f"{sample_id}:{field}={path}")

        if workflow_name == "alignment":
            reference_paths = ("star_index_DIR", "ref")
        else:
            reference_paths = ("ref", "GFF", "MAJIQ_license", "suppa2_events", "SALMON_INDEX")
            bam_dir = resolve_path(str(config["bam_dir"]), config_path)
            for sample_id in samples:
                bam = bam_dir / sample_id / f"{sample_id}_Aligned.sortedByCoord.out.bam"
                if not bam.is_file():
                    missing.append(f"{sample_id}:bam={bam}")

        for key in reference_paths:
            if not resolve_path(str(config[key]), config_path).exists():
                missing.append(f"{key}={resolve_path(str(config[key]), config_path)}")

        if missing:
            formatted = "\n  - ".join(missing)
            raise ValueError(f"Required input paths do not exist:\n  - {formatted}")

    print(f"Valid {workflow_name} configuration: {len(samples)} sample(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", choices=sorted(REQUIRED_KEYS))
    parser.add_argument("config", type=Path)
    parser.add_argument("--check-files", action="store_true")
    args = parser.parse_args()

    try:
        return validate(args.workflow, args.config.resolve(), args.check_files)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
