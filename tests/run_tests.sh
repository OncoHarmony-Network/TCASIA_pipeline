#!/usr/bin/env bash
set -euo pipefail

python -m unittest discover -s tests -p 'test_*.py'
python tests/prepare_fixtures.py
python scripts/validate_config.py alignment tests/config/alignment.yml --check-files
python scripts/validate_config.py as_calling tests/config/as_calling.yml --check-files
snakemake --lint -s workflows/01_alignment/Snakefile --configfile tests/config/alignment.yml
snakemake --lint -s workflows/02_as_calling/Snakefile --configfile tests/config/as_calling.yml
snakemake --dry-run --cores 1 -s workflows/01_alignment/Snakefile --configfile tests/config/alignment.yml
snakemake --dry-run --cores 1 -s workflows/02_as_calling/Snakefile --configfile tests/config/as_calling.yml
