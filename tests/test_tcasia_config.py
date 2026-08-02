from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "workflows" / "lib"))

from tcasia_config import load_samples, majiq_strandness, salmon_library_type


class SampleSheetTests(unittest.TestCase):
    def write_sheet(self, rows):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "samples.tsv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                delimiter="\t",
                fieldnames=("sample_id", "fastq_1", "fastq_2"),
            )
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_preserves_sample_ids_with_underscores(self):
        path = self.write_sheet(
            [{"sample_id": "patient_01", "fastq_1": "r1.fastq.gz", "fastq_2": "r2.fastq.gz"}]
        )
        self.assertEqual(list(load_samples(str(path))), ["patient_01"])

    def test_rejects_duplicate_sample_ids(self):
        row = {"sample_id": "sample_01", "fastq_1": "r1.fastq.gz", "fastq_2": "r2.fastq.gz"}
        path = self.write_sheet([row, row])
        with self.assertRaisesRegex(ValueError, "Duplicate sample_id"):
            load_samples(str(path))


class StrandnessMappingTests(unittest.TestCase):
    def test_firststrand_mapping(self):
        self.assertEqual(salmon_library_type("fr-firststrand"), "ISR")
        self.assertEqual(majiq_strandness("fr-firststrand"), "reverse")

    def test_unstranded_mapping(self):
        self.assertEqual(salmon_library_type("fr-unstranded"), "IU")
        self.assertEqual(majiq_strandness("fr-unstranded"), "none")


if __name__ == "__main__":
    unittest.main()
