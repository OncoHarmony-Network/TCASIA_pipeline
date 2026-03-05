# RNA-seq Alignment Workflow

This workflow performs quality control and alignment of paired-end RNA-seq data using STAR aligner.

## Overview

The alignment workflow consists of the following steps:

1. **STAR Alignment** - 2-pass alignment to GRCh38
2. **BAM Sorting** - Sort aligned reads by coordinate
3. **BAM Indexing** - Create BAM index for downstream analysis
4. **Gene Counting** - Quantify gene expression using featureCounts

## Input Requirements

### Data Format
- **Paired-end FASTQ files** (gzipped)
- Naming convention: `{sample}_1.fastq.gz` and `{sample}_2.fastq.gz`
- Quality: Phred33 encoding

### Reference Files
- **Genome**: GRCh38 primary assembly
- **Annotation**: GENCODE v34 GTF
- **STAR Index**: Pre-built for STAR v2.7.7a

## Configuration

Edit `config/config.yml`:

```yaml
cohort: YOUR_COHORT_NAME

root_DIR: /path/to/data

raw_DIR: /path/to/fastq

bam_DIR: /path/to/output/aligned

workdir: /path/to/output

star_index_DIR: /path/to/STAR_index

strandness: fr-firststrand  # or fr-secondstrand, fr-unstranded

read_len: 150  # Maximum read length in your data

ref: /path/to/gencode.v34.annotation.gtf

ref_fa: /path/to/GRCh38.primary_assembly.genome.fa
```

### Key Parameters

- **strandness**: Library preparation protocol
  - `fr-firststrand`: dUTP/NSR/NNSR (most common)
  - `fr-secondstrand`: Ligation-based
  - `fr-unstranded`: Unstranded libraries

- **read_len**: Use maximum read length if variable

## Usage

### 1. Prepare Configuration

```bash
cd workflows/01_alignment
cp config/config.yml config/my_config.yml
# Edit my_config.yml with your paths
```

### 2. Dry Run (Test)

```bash
snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 1 --use-conda --dry-run
```

### 3. Generate Workflow Diagram

```bash
snakemake -s Snakefile --configfile config/my_config.yml \
  --dag | dot -Tpdf > workflow_dag.pdf
```

### 4. Run Workflow

```bash
# Interactive mode
snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 10 --use-conda --rerun-incomplete

# Background mode
nohup snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 10 --use-conda --rerun-incomplete \
  > alignment.log 2>&1 &
```

## Output Structure

```
{bam_DIR}/
└── {sample}/
    ├── {sample}_Aligned.out.bam              # Unsorted BAM
    ├── {sample}_Aligned.sortedByCoord.out.bam  # Sorted BAM
    ├── {sample}_Aligned.sortedByCoord.out.bam.bai  # BAM index
    ├── {sample}_counts.txt                   # featureCounts output
    ├── {sample}_counts.id.txt                # Processed counts
    ├── {sample}_Log.final.out                # STAR alignment stats
    ├── {sample}_Log.out                      # STAR log
    ├── {sample}_Log.progress.out             # STAR progress
    └── {sample}_SJ.out.tab                   # Splice junctions
```

## STAR Parameters

```bash
STAR --runThreadN 10 \
     --genomeDir {STAR_INDEX} \
     --readFilesIn {R1} {R2} \
     --outFileNamePrefix {PREFIX} \
     --outSAMunmapped Within \
     --readFilesCommand zcat \
     --outFilterMismatchNmax 15 \
     --outSAMattributes All \
     --outStd Log \
     --limitBAMsortRAM 39050942993 \
     --outSAMtype BAM Unsorted \
     --outFilterIntronMotifs RemoveNoncanonical \
     --outSAMstrandField intronMotif \
     --twopassMode Basic \
     --quantMode GeneCounts
```

### Key Options Explained

- `--twopassMode Basic`: 2-pass alignment for improved splice junction detection
- `--outFilterMismatchNmax 15`: Allow up to 15 mismatches
- `--outFilterIntronMotifs RemoveNoncanonical`: Filter non-canonical junctions
- `--quantMode GeneCounts`: Generate gene-level counts

## Performance

### Resource Requirements

| Step | CPU | Memory | Time (per sample) |
|------|-----|--------|-------------------|
| STAR Alignment | 10 cores | 32 GB | 30-60 min |
| BAM Sorting | 30 cores | 8 GB | 10-20 min |
| BAM Indexing | 1 core | 2 GB | 5-10 min |
| featureCounts | 40 cores | 4 GB | 5-10 min |

### Optimization Tips

1. **Parallel Processing**: Increase `--cores` for multiple samples
2. **Memory**: Adjust `--limitBAMsortRAM` based on available RAM
3. **Disk I/O**: Use fast storage (SSD) for temporary files

## Troubleshooting

### Common Issues

**1. Out of Memory**
```
Error: STAR ran out of memory
```
**Solution**: Reduce `--limitBAMsortRAM` or increase system RAM

**2. STAR Index Mismatch**
```
Error: Genome version mismatch
```
**Solution**: Rebuild STAR index with the same STAR version

**3. Missing FASTQ Files**
```
Error: Input file not found
```
**Solution**: Check file paths and naming convention in config

**4. Conda Environment Issues**
```
Error: Environment creation failed
```
**Solution**: Update conda and retry
```bash
conda update -n base conda
```

## Quality Control

After alignment, check these metrics:

1. **Alignment Rate**: Should be >70% for good quality data
   - Check `{sample}_Log.final.out`

2. **Uniquely Mapped Reads**: Should be >60%
   - Check `Uniquely mapped reads %`

3. **Splice Junction Detection**:
   - Check `{sample}_SJ.out.tab` for novel junctions

## Next Steps

After successful alignment, proceed to:
- [AS Event Detection](../02_as_calling/README.md)
- Quality control analysis
- Differential expression analysis

## References

- **STAR**: Dobin et al., Bioinformatics 2013
- **featureCounts**: Liao et al., Bioinformatics 2014
- **GENCODE**: Frankish et al., Nucleic Acids Research 2019
