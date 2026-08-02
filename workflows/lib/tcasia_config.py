"""Shared configuration helpers for TCASIA Snakemake workflows."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Mapping


REQUIRED_SAMPLE_COLUMNS = ("sample_id", "fastq_1", "fastq_2")
VALID_STRANDNESS = {"fr-firststrand", "fr-secondstrand", "fr-unstranded"}


def load_samples(sample_sheet: str) -> Dict[str, Dict[str, str]]:
    """Load and validate the sample sheet used by both workflows."""
    path = Path(sample_sheet).expanduser()
    if not path.is_file():
        raise ValueError(f"Sample sheet does not exist: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing_columns = [column for column in REQUIRED_SAMPLE_COLUMNS if column not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(f"Sample sheet is missing columns: {', '.join(missing_columns)}")

        samples: Dict[str, Dict[str, str]] = {}
        for line_number, row in enumerate(reader, start=2):
            sample_id = (row.get("sample_id") or "").strip()
            if not sample_id:
                raise ValueError(f"Sample sheet line {line_number} has an empty sample_id")
            if sample_id in samples:
                raise ValueError(f"Duplicate sample_id in sample sheet: {sample_id}")

            record = {column: (row.get(column) or "").strip() for column in REQUIRED_SAMPLE_COLUMNS[1:]}
            empty_columns = [column for column, value in record.items() if not value]
            if empty_columns:
                raise ValueError(
                    f"Sample {sample_id} has empty fields: {', '.join(empty_columns)}"
                )
            samples[sample_id] = record

    if not samples:
        raise ValueError("Sample sheet must contain at least one sample")
    return samples


def require_config(config: Mapping[str, object], *keys: str) -> None:
    """Fail early when required top-level configuration values are absent."""
    missing = [key for key in keys if key not in config or config[key] in (None, "")]
    if missing:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing)}")


def normalize_strandness(value: str) -> str:
    """Validate the shared strandness vocabulary."""
    strandness = value.strip().lower()
    if strandness not in VALID_STRANDNESS:
        options = ", ".join(sorted(VALID_STRANDNESS))
        raise ValueError(f"Invalid strandness '{value}'. Expected one of: {options}")
    return strandness


def salmon_library_type(strandness: str) -> str:
    """Map shared strandness to Salmon paired-end library codes."""
    return {
        "fr-firststrand": "ISR",
        "fr-secondstrand": "ISF",
        "fr-unstranded": "IU",
    }[normalize_strandness(strandness)]


def majiq_strandness(strandness: str) -> str:
    """Map shared strandness to MAJIQ configuration values."""
    return {
        "fr-firststrand": "reverse",
        "fr-secondstrand": "forward",
        "fr-unstranded": "none",
    }[normalize_strandness(strandness)]
