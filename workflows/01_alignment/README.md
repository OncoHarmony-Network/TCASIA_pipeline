# Alignment Workflow

Runs fastp, STAR, samtools, and featureCounts for paired-end RNA-seq.

```bash
cp config/config.template.yml config/my_alignment.yml
cp config/samples.template.tsv config/samples.tsv

python ../../scripts/validate_config.py alignment config/my_alignment.yml --check-files
snakemake -s Snakefile --configfile config/my_alignment.yml \
  --cores 1 --use-conda --dry-run
snakemake -s Snakefile --configfile config/my_alignment.yml \
  --cores 16 --use-conda --rerun-incomplete
```

Primary outputs:

```text
{output_dir}/qc/{sample}_fastp.html
{output_dir}/aligned/{sample}/{sample}_Aligned.sortedByCoord.out.bam
{output_dir}/aligned/{sample}/{sample}_Aligned.sortedByCoord.out.bam.bai
{output_dir}/aligned/{sample}/{sample}_featureCounts.txt
```

Configuration: `config/config.template.yml`.
