# Usage Guide

This guide provides step-by-step instructions for running the TCASIA Alternative Splicing Analysis Pipeline.

## Prerequisites

Before starting, ensure you have:
- ✅ Completed [Installation Guide](installation.md)
- ✅ Reference files prepared
- ✅ FASTQ files ready
- ✅ Configuration files created

## Workflow Overview

```
Step 1: Prepare Input Files
    ↓
Step 2: Configure Workflow
    ↓
Step 3: Run Alignment (01_alignment)
    ↓
Step 4: Run AS Calling (02_as_calling)
    ↓
Step 5: Collect Results
```

## Step 1: Prepare Input Files

### 1.1 Organize FASTQ Files

```bash
# Create data directory
mkdir -p data/fastq

# Place your FASTQ files
# Expected naming: {sample}_R1.fastq.gz, {sample}_R2.fastq.gz
# Example:
#   sample1_R1.fastq.gz
#   sample1_R2.fastq.gz
#   sample2_R1.fastq.gz
#   sample2_R2.fastq.gz
```

### 1.2 Verify File Integrity

```bash
# Check file sizes
ls -lh data/fastq/*.fastq.gz

# Verify gzip integrity
gunzip -t data/fastq/*.fastq.gz

# Count reads (optional)
zcat data/fastq/sample1_R1.fastq.gz | echo $((`wc -l`/4))
```

## Step 2: Configure Workflow

### 2.1 Alignment Configuration

```bash
cd workflows/01_alignment

# Copy template
cp config/config.template.yml config/my_cohort.yml

# Edit configuration
nano config/my_cohort.yml
```

**Key parameters to modify:**

```yaml
cohort: YOUR_COHORT_NAME

root_DIR: /path/to/your/data

raw_DIR: /path/to/your/data/fastq

bam_DIR: /path/to/your/data/aligned

workdir: /path/to/your/data/AS_output

star_index_DIR: /path/to/references/STAR_index

strandness: fr-firststrand  # or fr-secondstrand, unstranded

read_len: 150  # Maximum read length

ref: /path/to/gencode.v34.annotation.gtf

ref_fa: /path/to/GRCh38.primary_assembly.genome.fa
```

### 2.2 AS Calling Configuration

```bash
cd workflows/02_as_calling

# Copy template
cp config/config.template.yml config/my_cohort.yml

# Edit configuration
nano config/my_cohort.yml
```

**Additional parameters:**

```yaml
MAJIQ_license: /path/to/majiq_license_academic_official.lic

suppa2_events: /path/to/gencode.v34.events.ioe

SALMON_INDEX: /path/to/gencode.v34.transcripts.salmon.index

GFF: /path/to/gencode.v34.annotation.gff3
```

## Step 3: Run Alignment Workflow

### 3.1 Dry Run (Test)

```bash
cd workflows/01_alignment

# Activate snakemake environment
micromamba activate snakemake

# Test workflow
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --dry-run \
  --printshellcmds
```

### 3.2 Execute Alignment

```bash
# Run with 10 cores
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cores 10 \
  --use-conda \
  --keep-going

# Or with more detailed logging
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cores 10 \
  --use-conda \
  --keep-going \
  --printshellcmds \
  --reason \
  2>&1 | tee alignment.log
```

**Resource recommendations:**
- **Cores**: 8-16 per sample
- **Memory**: 32 GB minimum
- **Time**: ~2-4 hours per sample (150M reads)

### 3.3 Monitor Progress

```bash
# Check running jobs
ps aux | grep STAR

# Monitor disk usage
df -h

# View logs
tail -f logs/STAR/{sample}.log
```

### 3.4 Verify Alignment Output

```bash
# Check BAM files
ls -lh {bam_DIR}/*.bam

# Alignment statistics
samtools flagstat {bam_DIR}/sample1.Aligned.sortedByCoord.out.bam

# Count aligned reads
samtools view -c -F 260 {bam_DIR}/sample1.Aligned.sortedByCoord.out.bam
```

## Step 4: Run AS Calling Workflow

### 4.1 Dry Run (Test)

```bash
cd workflows/02_as_calling

# Test workflow
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --dry-run \
  --printshellcmds
```

### 4.2 Execute AS Calling

```bash
# Run with 40 cores (4 algorithms in parallel)
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cores 40 \
  --use-conda \
  --keep-going \
  --printshellcmds \
  2>&1 | tee as_calling.log
```

**Resource recommendations:**
- **Cores**: 40+ (10 per algorithm)
- **Memory**: 64 GB minimum
- **Time**: ~4-8 hours per cohort (10 samples)

### 4.3 Monitor AS Calling

```bash
# Check running processes
ps aux | grep -E "rmats|majiq|suppa|spladder"

# View algorithm-specific logs
tail -f logs/rmats/{cohort}.log
tail -f logs/MAJIQ/{cohort}.log
tail -f logs/SUPPA2/{cohort}.log
tail -f logs/spladder/{cohort}.log
```

## Step 5: Collect Results

### 5.1 Output Structure

```
workdir/
├── rmats/
│   ├── SE.MATS.JC.txt          # Skipped exon events
│   ├── A5SS.MATS.JC.txt        # Alternative 5' splice site
│   ├── A3SS.MATS.JC.txt        # Alternative 3' splice site
│   ├── MXE.MATS.JC.txt         # Mutually exclusive exons
│   └── RI.MATS.JC.txt          # Retained intron
├── MAJIQ/
│   ├── build/                  # MAJIQ build output
│   └── psi/                    # PSI quantification
├── SUPPA2/
│   ├── {cohort}_SE.psi         # Event-level PSI
│   ├── {cohort}_A5.psi
│   ├── {cohort}_A3.psi
│   ├── {cohort}_MX.psi
│   └── {cohort}_RI.psi
└── spladder/
    └── merge_graphs_{cohort}/
        ├── exon_skip_C3.confirmed.txt
        ├── intron_retention_C3.confirmed.txt
        └── ...
```

### 5.2 Verify Outputs

```bash
# Check rMATS output
wc -l workdir/rmats/SE.MATS.JC.txt

# Check MAJIQ output
ls -lh workdir/MAJIQ/psi/*.tsv

# Check SUPPA2 output
head workdir/SUPPA2/{cohort}_SE.psi

# Check SplAdder output
ls -lh workdir/spladder/merge_graphs_{cohort}/*.txt
```

### 5.3 Summary Statistics

```bash
# Count events per algorithm
echo "rMATS SE events:"
tail -n +2 workdir/rmats/SE.MATS.JC.txt | wc -l

echo "SUPPA2 SE events:"
tail -n +2 workdir/SUPPA2/{cohort}_SE.psi | wc -l

echo "SplAdder exon skip events:"
tail -n +2 workdir/spladder/merge_graphs_{cohort}/exon_skip_C3.confirmed.txt | wc -l
```

## Advanced Usage

### Parallel Execution on HPC

```bash
# SLURM cluster
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cluster "sbatch -p normal -n {threads} --mem={resources.mem_mb}" \
  --jobs 10 \
  --use-conda

# PBS cluster
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cluster "qsub -l nodes=1:ppn={threads},mem={resources.mem_mb}mb" \
  --jobs 10 \
  --use-conda
```

### Resume Failed Jobs

```bash
# Snakemake automatically resumes from last checkpoint
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --cores 40 \
  --use-conda \
  --keep-going \
  --rerun-incomplete
```

### Generate Workflow Visualization

```bash
# Create DAG (Directed Acyclic Graph)
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --dag | dot -Tpdf > workflow_dag.pdf

# Create rule graph
snakemake -s Snakefile \
  --configfile config/my_cohort.yml \
  --rulegraph | dot -Tpdf > workflow_rules.pdf
```

## Troubleshooting

### Common Issues

**Issue**: STAR alignment fails with "out of memory"
```bash
# Solution: Reduce --limitBAMsortRAM in Snakefile
# Or increase system memory
```

**Issue**: rMATS fails with "read length mismatch"
```bash
# Solution: Verify read_len in config matches actual data
# Run: zcat sample_R1.fastq.gz | head -2 | tail -1 | wc -c
```

**Issue**: MAJIQ license error
```bash
# Solution: Verify license path in config
# Check: cat /path/to/majiq_license_academic_official.lic
```

**Issue**: Conda environment creation fails
```bash
# Solution: Use micromamba instead of conda
# Or: conda clean --all && conda update conda
```

### Performance Optimization

**Slow STAR alignment:**
- Use `--limitBAMsortRAM` to control memory
- Increase `--runThreadN` for more cores
- Use local SSD for temporary files

**Slow AS calling:**
- Run algorithms in parallel (increase `--cores`)
- Use `--keep-going` to continue on errors
- Pre-build conda environments

## Next Steps

After successful execution:
1. **Quality Control**: Check alignment rates, event counts
2. **Downstream Analysis**: Filter events, calculate ΔPSI, statistical testing
3. **Integration**: Combine results from multiple algorithms
4. **Visualization**: Generate plots for publication

## Support

- **Documentation**: [Full Documentation](../docs/)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline/issues)
- **Contact**: jianguo.zhou@zmu.edu.cn
