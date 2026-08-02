# Method Verification

| Step | Version | Key implementation |
|---|---:|---|
| fastp | 0.23.4 | Configurable quality and length filters |
| STAR | 2.7.7a | Two-pass alignment; mismatch and splice-junction filters |
| samtools | 1.15 | Coordinate sorting and indexing |
| featureCounts | 2.0.1 | Paired-end exon counting by `gene_id` |
| rMATS | 4.3.0 | Paired-end, strand-aware, variable read length, `--statoff` |
| MAJIQ | 2.5 | Sample-specific build, `minreads=10`, Voila export |
| SUPPA2 | 2.3 | Salmon 1.10.3 quantification and `psiPerEvent -f 1` |
| SplAdder | 3.1.1 | Confidence 3 and configured canonical event types |

Shared inputs are defined by `sample_id`, `fastq_1`, and `fastq_2`. Strandness is mapped in `workflows/lib/tcasia_config.py`.

Verification:

```bash
bash tests/run_tests.sh
```
