# AS-calling Workflow

Runs rMATS 4.3.0, MAJIQ 2.5, SUPPA2 2.3, Salmon 1.10.3, and SplAdder 3.1.1 per sample.

```bash
cp config/config.template.yml config/my_as_calling.yml
cp config/samples.template.tsv config/samples.tsv

python ../../scripts/validate_config.py as_calling config/my_as_calling.yml --check-files
snakemake -s Snakefile --configfile config/my_as_calling.yml \
  --cores 1 --use-conda --dry-run
snakemake -s Snakefile --configfile config/my_as_calling.yml \
  --cores 40 --use-conda --rerun-incomplete --keep-going
```

Expected BAM path:

```text
{bam_dir}/{sample_id}/{sample_id}_Aligned.sortedByCoord.out.bam
```

Primary output directories:

```text
{output_dir}/{sample}/rmats/
{output_dir}/{sample}/majiq/
{output_dir}/{sample}/suppa2/
{output_dir}/{sample}/spladder/
```

Configuration: `config/config.template.yml`.
