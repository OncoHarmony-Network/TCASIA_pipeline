# Troubleshooting

## First checks

```bash
python scripts/validate_config.py alignment CONFIG --check-files
python scripts/validate_config.py as_calling CONFIG --check-files
snakemake -s SNAKEFILE --configfile CONFIG --cores 1 --dry-run --printshellcmds
```

Rule logs are under `{output_dir}/logs`.

## Paths

Run Snakemake from the workflow directory. Use absolute paths for FASTQ, BAM, reference, license, and output locations.

AS BAM layout:

```text
{bam_dir}/{sample_id}/{sample_id}_Aligned.sortedByCoord.out.bam
```

## References

Use one genome and annotation release for STAR, GTF, GFF3, Salmon, and SUPPA2 events. Set `read_len` from:

```bash
bash scripts/read_length.sh /path/to/sample.bam
```

## Resume

```bash
snakemake -s Snakefile --configfile CONFIG \
  --cores 16 --use-conda --rerun-incomplete --keep-going
```

For support, open an issue at:

https://github.com/OncoHarmony-Network/TCASIA_pipeline/issues
