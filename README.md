# TCASIA Alternative Splicing Pipeline

[![Snakemake](https://img.shields.io/badge/snakemake-%E2%89%A57.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Snakemake workflows for paired-end RNA-seq alignment and alternative-splicing calling with rMATS, MAJIQ, SUPPA2, and SplAdder.

## Workflows

```text
FASTQ
  -> fastp -> STAR -> samtools -> featureCounts
  -> rMATS | MAJIQ | SUPPA2 | SplAdder
```

Both workflows use the same tab-separated sample sheet:

```text
sample_id	fastq_1	fastq_2
sample_01	/path/sample_01_1.fastq.gz	/path/sample_01_2.fastq.gz
```

## Setup

```bash
git clone https://github.com/OncoHarmony-Network/TCASIA_pipeline.git
cd TCASIA_pipeline
micromamba create -f environment.yml
micromamba activate tcasia-workflow
```

Reference settings: GRCh38 primary assembly and GENCODE v34.

## Run alignment

```bash
cd workflows/01_alignment
cp config/config.template.yml config/my_alignment.yml
cp config/samples.template.tsv config/samples.tsv

python ../../scripts/validate_config.py alignment config/my_alignment.yml --check-files
snakemake -s Snakefile --configfile config/my_alignment.yml --cores 16 --use-conda
```

## Run AS calling

```bash
cd ../02_as_calling
cp config/config.template.yml config/my_as_calling.yml
cp config/samples.template.tsv config/samples.tsv

python ../../scripts/validate_config.py as_calling config/my_as_calling.yml --check-files
snakemake -s Snakefile --configfile config/my_as_calling.yml --cores 40 --use-conda
```

## Tests

```bash
bash tests/run_tests.sh
```

## Documentation

- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Parameters](docs/parameters.md)
- [Outputs](docs/output_format.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Method verification](METHOD_VERIFICATION.md)
- [Citation](CITATION.md)

Issues: https://github.com/OncoHarmony-Network/TCASIA_pipeline/issues

License: [MIT](LICENSE)
