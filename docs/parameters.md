# Parameters

The configuration templates are the source of truth:

- `workflows/01_alignment/config/config.template.yml`
- `workflows/02_as_calling/config/config.template.yml`

## Shared fields

Sample sheet columns: `sample_id`, `fastq_1`, `fastq_2`.

| `strandness` | rMATS | Salmon | MAJIQ |
|---|---|---|---|
| `fr-firststrand` | `fr-firststrand` | `ISR` | `reverse` |
| `fr-secondstrand` | `fr-secondstrand` | `ISF` | `forward` |
| `fr-unstranded` | `fr-unstranded` | `IU` | `none` |

## Alignment

Required: `samples`, `output_dir`, `star_index_DIR`, `ref`, `strandness`.

| Key | Default |
|---|---:|
| `threads.fastp` | 8 |
| `threads.star` | 10 |
| `threads.samtools_sort` | 8 |
| `threads.samtools_index` | 2 |
| `threads.featurecounts` | 8 |
| `fastp.min_length` | 36 |
| `fastp.qualified_quality_phred` | 20 |
| `fastp.unqualified_percent_limit` | 40 |
| `fastp.n_base_limit` | 5 |
| `star.out_filter_mismatch_nmax` | 15 |
| `star.limit_bam_sort_ram` | 39050942993 |

## AS calling

Required: `samples`, `output_dir`, `bam_dir`, `ref`, `GFF`, `MAJIQ_license`, `suppa2_events`, `SALMON_INDEX`, `read_len`, `strandness`.

| Key | Default |
|---|---:|
| `threads.rmats` | 10 |
| `threads.majiq` | 8 |
| `threads.voila` | 4 |
| `threads.salmon` | 8 |
| `threads.spladder` | 8 |
| `rmats.cstat` | 0.0001 |
| `rmats.extra` | `""` |
| `majiq.genome` | `hg38` |
| `majiq.minreads` | 10 |
| `suppa2.min_tpm` | 1 |
| `spladder.confidence` | 3 |
| `spladder.merge_strategy` | `single` |

Default SplAdder event types:

```text
exon_skip,intron_retention,alt_3prime,alt_5prime,mutex_exons
```

Validate configuration with `scripts/validate_config.py` before running Snakemake.
