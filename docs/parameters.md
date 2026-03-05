# Parameter Reference

Complete reference for all configurable parameters in the TCASIA Alternative Splicing Analysis Pipeline.

## Configuration File Structure

Configuration files use YAML format with the following sections:
- **Cohort Information**: Project metadata
- **Directory Paths**: Input/output locations
- **Reference Files**: Genome and annotation paths
- **Sequencing Parameters**: Library-specific settings
- **Tool-Specific Parameters**: Algorithm configurations

---

## Alignment Workflow Parameters

### Required Parameters

#### `cohort`
- **Type**: String
- **Description**: Cohort or project identifier
- **Example**: `PRJNA498500`, `LUAD_ICI`
- **Usage**: Used for naming output files and directories

#### `root_DIR`
- **Type**: Path (absolute)
- **Description**: Root directory for all data
- **Example**: `/data/IO_RNA`
- **Notes**: Must have read/write permissions

#### `raw_DIR`
- **Type**: Path (absolute)
- **Description**: Directory containing raw FASTQ files
- **Example**: `/data/IO_RNA/PRJNA498500/fq`
- **Expected files**: `{sample}_R1.fastq.gz`, `{sample}_R2.fastq.gz`

#### `bam_DIR`
- **Type**: Path (absolute)
- **Description**: Output directory for aligned BAM files
- **Example**: `/data/IO_RNA/AS/PRJNA498500/aligned`
- **Created files**: `{sample}.Aligned.sortedByCoord.out.bam`

#### `workdir`
- **Type**: Path (absolute)
- **Description**: Working directory for intermediate and final outputs
- **Example**: `/data/IO_RNA/AS/PRJNA498500`
- **Subdirectories**: `logs/`, `benchmarks/`, `qc/`

#### `star_index_DIR`
- **Type**: Path (absolute)
- **Description**: STAR genome index directory
- **Example**: `/data/reference/hg38/STAR_index_star_2.7.7a`
- **Requirements**: Pre-built with STAR 2.7.7a, GRCh38, GENCODE v34

#### `strandness`
- **Type**: String (enum)
- **Options**:
  - `fr-firststrand`: First-strand (dUTP) libraries (most common)
  - `fr-secondstrand`: Second-strand libraries
  - `unstranded`: Non-stranded libraries
- **Description**: Library strandness protocol
- **How to determine**: Use RSeQC `infer_experiment.py`
- **Example**: `fr-firststrand`

#### `read_len`
- **Type**: Integer
- **Description**: Maximum read length in dataset
- **Example**: `150` (for 150bp reads)
- **Notes**:
  - If variable, use maximum value
  - Critical for rMATS parameter `--readLength`
  - Affects STAR `--sjdbOverhang` (read_len - 1)

#### `ref`
- **Type**: Path (absolute)
- **Description**: Reference transcriptome GTF file
- **Example**: `/data/reference/hg38/gencode.v34.annotation.gtf`
- **Format**: GTF (Gene Transfer Format)
- **Source**: GENCODE v34

#### `ref_fa`
- **Type**: Path (absolute)
- **Description**: Reference genome FASTA file
- **Example**: `/data/reference/hg38/GRCh38.primary_assembly.genome.fa`
- **Format**: FASTA (uncompressed)
- **Source**: GRCh38 primary assembly

---

## AS Calling Workflow Parameters

### Required Parameters (in addition to alignment parameters)

#### `MAJIQ_license`
- **Type**: Path (absolute)
- **Description**: MAJIQ academic license file
- **Example**: `/path/to/majiq_license_academic_official.lic`
- **How to obtain**: https://majiq.biociphers.org/
- **Notes**: Required for MAJIQ execution

#### `suppa2_events`
- **Type**: Path (absolute)
- **Description**: Pre-generated SUPPA2 event file
- **Example**: `/data/reference/hg38/gencode.v34.events.ioe`
- **Format**: IOE (Isoform-centric Event)
- **Generation**: `suppa.py generateEvents -i ref.gtf -o events -f ioe -e SE SS MX RI FL`

#### `SALMON_INDEX`
- **Type**: Path (absolute)
- **Description**: Salmon transcriptome index directory
- **Example**: `/data/reference/hg38/gencode.v34.transcripts.salmon.index`
- **Requirements**: Built with Salmon 1.10.3, GENCODE v34 transcripts

#### `GFF`
- **Type**: Path (absolute)
- **Description**: Reference annotation in GFF3 format (for MAJIQ)
- **Example**: `/data/reference/hg38/gencode.v34.annotation.gff3`
- **Format**: GFF3 (General Feature Format version 3)
- **Source**: GENCODE v34

---

## Tool-Specific Parameters

### STAR Alignment

**Key parameters** (defined in Snakefile):

```python
--runThreadN {threads}              # CPU cores (default: 16)
--genomeDir {star_index_DIR}        # Index directory
--readFilesIn {R1} {R2}             # Input FASTQ files
--readFilesCommand zcat             # Decompress gzipped files
--outFileNamePrefix {prefix}        # Output file prefix
--outSAMtype BAM SortedByCoordinate # Output sorted BAM
--twopassMode Basic                 # 2-pass alignment (recommended)
--outFilterMultimapNmax 20          # Max multi-mapping locations
--alignSJoverhangMin 8              # Min overhang for splice junctions
--alignSJDBoverhangMin 1            # Min overhang for annotated junctions
--outFilterMismatchNmax 999         # Max mismatches (filter by ratio)
--outFilterMismatchNoverReadLmax 0.04  # Max mismatch ratio (4%)
--alignIntronMin 20                 # Min intron length
--alignIntronMax 1000000            # Max intron length
--alignMatesGapMax 1000000          # Max gap between mates
--limitBAMsortRAM 31000000000       # RAM for BAM sorting (31 GB)
```

**Customization**: Edit `workflows/01_alignment/Snakefile` rule `star_align`

### rMATS

**Key parameters** (defined in Snakefile):

```python
--b1 {bam_list_group1}              # BAM files for group 1
--b2 {bam_list_group2}              # BAM files for group 2 (optional)
--gtf {ref}                         # GTF annotation
--readLength {read_len}             # Read length
--variable-read-length              # Allow variable read lengths
--nthread {threads}                 # CPU cores (default: 10)
--od {output_dir}                   # Output directory
--tmp {temp_dir}                    # Temporary directory
--cstat 0.0001                      # Cutoff for splicing difference (CRITICAL)
--libType fr-firststrand            # Library type
```

**Critical parameter**: `--cstat 0.0001`
- Controls sensitivity of differential splicing detection
- Lower values = more sensitive (more events detected)
- TCASIA uses 0.0001 for high sensitivity

**Customization**: Edit `workflows/02_as_calling/rules/rmats.smk`

### MAJIQ

**Key parameters** (defined in Snakefile):

```python
# Build step
majiq build {gff3} \
  -c {config_file} \
  -j {threads} \
  -o {output_dir} \
  --minreads 10                     # Min reads supporting junction (CRITICAL)

# PSI step
majiq psi {majiq_files} \
  -j {threads} \
  -o {output_dir} \
  -n {sample_names}
```

**Critical parameter**: `--minreads 10`
- Minimum reads required to support a splice junction
- Higher values = more stringent (fewer events)
- TCASIA uses 10 for balance between sensitivity and reliability

**Configuration file** (`majiq_config.txt`):
```
[info]
readlen={read_len}
bamdirs={bam_dir}
genome=hg38
strandness={strandness}

[experiments]
sample1=sample1
sample2=sample2
...
```

**Customization**: Edit `workflows/02_as_calling/rules/MAJIQ.smk`

### SUPPA2

**Key parameters** (defined in Snakefile):

```python
# Salmon quantification
salmon quant \
  -i {SALMON_INDEX} \
  -l A \                            # Auto-detect library type
  -1 {R1} -2 {R2} \
  -o {output_dir} \
  -p {threads} \
  --gcBias \                        # GC bias correction (recommended)
  --validateMappings                # Validate mappings

# PSI calculation
suppa.py psiPerEvent \
  -i {suppa2_events} \
  -e {transcript_tpm} \
  -o {output_prefix} \
  -f 1                              # Min TPM threshold (CRITICAL)
```

**Critical parameter**: `-f 1`
- Minimum TPM (Transcripts Per Million) threshold
- Filters low-expression transcripts
- TCASIA uses 1 TPM for inclusion

**Customization**: Edit `workflows/02_as_calling/rules/SUPPA2.smk`

### SplAdder

**Key parameters** (defined in Snakefile):

```python
spladder build \
  -b {bam_files} \
  -o {output_dir} \
  -a {gtf} \
  --parallel {threads} \
  --merge-strat single \            # Merge strategy
  --event-types exon_skip,intron_retention,alt_3prime,alt_5prime,mutex_exons \
  --confidence 3                    # Confidence level (default)
```

**Confidence levels**:
- `1`: Low confidence (more events, less reliable)
- `2`: Medium confidence
- `3`: High confidence (fewer events, more reliable) - **TCASIA default**

**Customization**: Edit `workflows/02_as_calling/rules/spladder.smk`

---

## Resource Requirements

### Per-Sample Requirements

| Step | CPU Cores | Memory | Time | Disk Space |
|------|-----------|--------|------|------------|
| STAR Alignment | 16 | 32 GB | 2-4h | 20-30 GB |
| rMATS | 10 | 16 GB | 1-2h | 5 GB |
| MAJIQ Build | 8 | 16 GB | 1-2h | 5 GB |
| SUPPA2 | 8 | 8 GB | 30min | 2 GB |
| SplAdder | 8 | 16 GB | 1-2h | 5 GB |

**Notes**:
- Times based on ~150M paired-end reads
- Disk space includes intermediate files
- Memory requirements scale with genome size

### Cohort-Level Requirements

For a 10-sample cohort:
- **Total disk**: 300-500 GB
- **Peak memory**: 64 GB (parallel AS calling)
- **Total time**: 1-2 days (with parallelization)

---

## Environment Variables

### Optional Environment Variables

```bash
# Temporary directory (for large intermediate files)
export TMPDIR=/scratch/tmp

# Conda cache directory
export CONDA_PKGS_DIRS=/scratch/conda_cache

# Snakemake directory
export SNAKEMAKE_OUTPUT_CACHE=/scratch/snakemake_cache
```

---

## Advanced Configuration

### Custom Snakemake Parameters

```bash
# Increase job retries
snakemake --retries 3

# Set maximum jobs
snakemake --jobs 10

# Use specific conda prefix
snakemake --conda-prefix /path/to/conda/envs

# Detailed logging
snakemake --verbose --printshellcmds --reason

# Cluster execution
snakemake --cluster "sbatch -p normal -n {threads}"
```

### Performance Tuning

**For large cohorts (>50 samples)**:
- Increase `--cores` to 100+
- Use cluster execution with `--cluster`
- Enable `--keep-going` to continue on failures
- Use `--rerun-incomplete` to resume

**For limited resources**:
- Reduce `--cores` to 4-8
- Decrease `--limitBAMsortRAM` in STAR
- Run algorithms sequentially (not in parallel)

---

## Parameter Validation

### Pre-Flight Checklist

Before running, verify:

```bash
# Check read length
zcat {raw_DIR}/sample1_R1.fastq.gz | head -2 | tail -1 | wc -c

# Check strandness
infer_experiment.py -r {ref_bed} -i {bam_file}

# Verify reference files exist
ls -lh {star_index_DIR}
ls -lh {ref}
ls -lh {ref_fa}
ls -lh {GFF}
ls -lh {SALMON_INDEX}
ls -lh {suppa2_events}

# Check MAJIQ license
cat {MAJIQ_license}
```

---

## Troubleshooting Parameters

### Common Parameter Issues

**Issue**: STAR fails with "genome mismatch"
```yaml
# Solution: Rebuild STAR index with correct --sjdbOverhang
--sjdbOverhang: {read_len - 1}
```

**Issue**: rMATS reports "read length mismatch"
```yaml
# Solution: Set read_len to maximum in dataset
read_len: 150  # Use maximum, not average
```

**Issue**: MAJIQ fails with "strandness error"
```yaml
# Solution: Verify strandness with RSeQC
# fr-firststrand: Sense reads from reverse strand
# fr-secondstrand: Sense reads from forward strand
```

**Issue**: SUPPA2 produces no events
```yaml
# Solution: Lower TPM threshold
-f 0.5  # Instead of -f 1
```

---

## References

- **STAR**: Dobin et al., Bioinformatics 2013
- **rMATS**: Shen et al., PNAS 2014
- **MAJIQ**: Vaquero-Garcia et al., eLife 2016
- **SUPPA2**: Trincado et al., Genome Biology 2018
- **SplAdder**: Kahles et al., Genome Biology 2016

---

## Support

For parameter-related questions:
- **Documentation**: [Full Documentation](../docs/)
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline/issues)
- **Contact**: jianguo.zhou@zmu.edu.cn
