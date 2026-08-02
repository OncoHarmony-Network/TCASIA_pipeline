# Installation

## Requirements

- Linux
- Git
- Conda, Mamba, or Micromamba
- Snakemake 7.0 or newer

## Environment

```bash
git clone https://github.com/OncoHarmony-Network/TCASIA_pipeline.git
cd TCASIA_pipeline
micromamba create -f environment.yml
micromamba activate tcasia-workflow
```

Tool environments are created from each workflow's `envs/` directory when Snakemake runs with `--use-conda`.

## References

Prepare matching GRCh38/GENCODE v34 resources:

- GRCh38 primary assembly FASTA
- GENCODE v34 GTF
- GENCODE v34 GFF3
- STAR 2.7.7a genome index
- GENCODE v34 transcript FASTA and Salmon index
- SUPPA2 IOE events generated from the same GTF
- MAJIQ academic license

For STAR, set `--sjdbOverhang` to maximum read length minus one when building the index.

## Configuration

```bash
cp workflows/01_alignment/config/config.template.yml \
  workflows/01_alignment/config/my_alignment.yml
cp workflows/01_alignment/config/samples.template.tsv \
  workflows/01_alignment/config/samples.tsv

cp workflows/02_as_calling/config/config.template.yml \
  workflows/02_as_calling/config/my_as_calling.yml
cp workflows/02_as_calling/config/samples.template.tsv \
  workflows/02_as_calling/config/samples.tsv
```

Edit the copied YAML and TSV files, then follow [Usage](usage.md).
