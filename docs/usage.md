# Usage

## Sample sheet

Both workflows use `config/samples.tsv`:

```text
sample_id	fastq_1	fastq_2
sample_01	/data/fastq/sample_01_1.fastq.gz	/data/fastq/sample_01_2.fastq.gz
```

Sample IDs must be unique. Absolute input and reference paths are recommended.

## Alignment

Edit `workflows/01_alignment/config/my_alignment.yml` from the template. Required keys:

```yaml
samples: config/samples.tsv
output_dir: /data/project/alignment
star_index_DIR: /data/reference/STAR_index
ref: /data/reference/gencode.v34.annotation.gtf
strandness: fr-firststrand
```

Run from `workflows/01_alignment`:

```bash
python ../../scripts/validate_config.py alignment config/my_alignment.yml --check-files
snakemake -s Snakefile --configfile config/my_alignment.yml \
  --cores 1 --use-conda --dry-run
snakemake -s Snakefile --configfile config/my_alignment.yml \
  --cores 16 --use-conda --rerun-incomplete
```

## AS calling

Edit `workflows/02_as_calling/config/my_as_calling.yml` from the template. Required keys:

```yaml
samples: config/samples.tsv
output_dir: /data/project/as_calling
bam_dir: /data/project/alignment/aligned
ref: /data/reference/gencode.v34.annotation.gtf
GFF: /data/reference/gencode.v34.annotation.gff3
MAJIQ_license: /data/license/majiq_license_academic_official.lic
suppa2_events: /data/reference/gencode.v34.events.ioe
SALMON_INDEX: /data/reference/gencode.v34.salmon.index
read_len: 150
strandness: fr-firststrand
```

Expected BAM path:

```text
{bam_dir}/{sample_id}/{sample_id}_Aligned.sortedByCoord.out.bam
```

Check read length with:

```bash
bash ../../scripts/read_length.sh /path/to/sample.bam
```

Run from `workflows/02_as_calling`:

```bash
python ../../scripts/validate_config.py as_calling config/my_as_calling.yml --check-files
snakemake -s Snakefile --configfile config/my_as_calling.yml \
  --cores 1 --use-conda --dry-run
snakemake -s Snakefile --configfile config/my_as_calling.yml \
  --cores 40 --use-conda --rerun-incomplete --keep-going
```

Strandness values: `fr-firststrand`, `fr-secondstrand`, or `fr-unstranded`.

See [Parameters](parameters.md) and [Outputs](output_format.md).
