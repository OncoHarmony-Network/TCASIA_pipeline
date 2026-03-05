# Installation Guide

This guide provides detailed instructions for installing the TCASIA Alternative Splicing Analysis Pipeline.

## System Requirements

### Hardware
- **CPU**: Multi-core processor (≥8 cores recommended)
- **RAM**: ≥16 GB (32 GB recommended for large datasets)
- **Storage**: Varies by cohort size
  - Per sample: ~30-50 GB
    - FASTQ files: ~3-5 GB
    - BAM files: ~15-25 GB
    - AS outputs: ~5-10 GB
  - Reference files: ~30 GB (shared across cohort)
  - **Example**: 10-sample cohort ≈ 300-500 GB total

### Operating System
- Linux (tested on Ubuntu 20.04+, CentOS 7+)
- macOS (limited testing, not recommended for production)
- Windows: Not supported (use WSL2)

### Software Prerequisites
- **Conda**, **Mamba**, or **Micromamba** (package manager)
- **Git** (for cloning repository)
- **Graphviz** (optional, for workflow visualization)

## Installation Steps

### 1. Install Conda/Mamba/Micromamba

If you don't have a package manager installed:

**Option 1: Micromamba (Recommended - Fastest)**

```bash
# Download and install Micromamba
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)

# Restart shell
source ~/.bashrc  # or ~/.zshrc
```

**Option 2: Miniconda**

```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Follow prompts and restart shell
source ~/.bashrc
```

**Option 3: Mamba (via Conda)**

```bash
# If you already have conda
conda install -n base -c conda-forge mamba
```

### 2. Clone Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TCASIA_AS_Pipeline.git
cd TCASIA_AS_Pipeline
```

### 3. Create Snakemake Environment

```bash
# Using micromamba (recommended)
micromamba create -c conda-forge -c bioconda -n snakemake snakemake

# Or using mamba (faster than conda)
mamba create -c conda-forge -c bioconda -n snakemake snakemake

# Or using conda
conda create -c conda-forge -c bioconda -n snakemake snakemake

# Activate environment
micromamba activate snakemake  # or: conda activate snakemake

# Verify installation
snakemake --version  # Should show ≥7.0.0
```

### 4. Prepare Reference Files

#### 4.1 Download Reference Genome

```bash
# Create reference directory
mkdir -p references/hg38

cd references/hg38

# Download GRCh38 primary assembly
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_34/GRCh38.primary_assembly.genome.fa.gz
gunzip GRCh38.primary_assembly.genome.fa.gz

# Index genome (for STAR)
samtools faidx GRCh38.primary_assembly.genome.fa
```

#### 4.2 Download GENCODE Annotation

```bash
# GTF format (for STAR, rMATS, SplAdder, SUPPA2)
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_34/gencode.v34.annotation.gtf.gz
gunzip gencode.v34.annotation.gtf.gz

# GFF3 format (for MAJIQ)
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_34/gencode.v34.annotation.gff3.gz
gunzip gencode.v34.annotation.gff3.gz

# Transcripts FASTA (for Salmon)
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_34/gencode.v34.transcripts.fa.gz
gunzip gencode.v34.transcripts.fa.gz
```

#### 4.3 Build STAR Index

```bash
# Create STAR environment
micromamba create -n star -c bioconda star=2.7.7a
micromamba activate star

# Build index (requires ~32 GB RAM)
mkdir -p STAR_index

STAR --runMode genomeGenerate \
     --genomeDir STAR_index \
     --genomeFastaFiles GRCh38.primary_assembly.genome.fa \
     --sjdbGTFfile gencode.v34.annotation.gtf \
     --sjdbOverhang 149 \
     --runThreadN 16

micromamba deactivate
```

**Note**: `--sjdbOverhang` should be (read_length - 1). Use 149 for 150bp reads.

#### 4.4 Build Salmon Index

```bash
# Create Salmon environment
micromamba create -n salmon -c bioconda salmon=1.10.3
micromamba activate salmon

# Build index
salmon index -t gencode.v34.transcripts.fa \
             -i gencode.v34.transcripts.salmon.index \
             -k 31 \
             -p 16

micromamba deactivate
```

#### 4.5 Generate SUPPA2 Events

```bash
# Create SUPPA2 environment
micromamba create -n suppa2 -c bioconda suppa=2.3
micromamba activate suppa2

# Generate events
suppa.py generateEvents \
         -i gencode.v34.annotation.gtf \
         -o gencode.v34.events \
         -f ioe \
         -e SE SS MX RI FL

micromamba deactivate
```

### 5. Obtain MAJIQ License

MAJIQ requires an academic license:

1. Visit: https://majiq.biociphers.org/
2. Request academic license
3. Download license file: `majiq_license_academic_official.lic`
4. Place in `workflows/02_as_calling/scripts/`

### 6. Verify Installation

```bash
# Activate snakemake environment
micromamba activate snakemake

# Test workflow syntax
cd workflows/01_alignment
snakemake -s Snakefile --dry-run

cd ../02_as_calling
snakemake -s Snakefile --dry-run
```

## Environment Configuration

### Conda Environments

The pipeline automatically creates tool-specific environments:

- **ega**: STAR, samtools, subread
- **rmats**: rMATS
- **MAJIQ**: MAJIQ, voila
- **SUPPA2**: SUPPA2, salmon
- **spladder**: SplAdder

These are created on first run via `--use-conda` flag.

### Manual Environment Creation (Optional)

To pre-build environments:

```bash
# Alignment tools
micromamba env create -f workflows/01_alignment/envs/ega.yaml
micromamba env create -f workflows/01_alignment/envs/samtools1.yaml

# AS calling tools
micromamba env create -f workflows/02_as_calling/envs/rmats.yaml
micromamba env create -f workflows/02_as_calling/envs/MAJIQ.yaml
micromamba env create -f workflows/02_as_calling/envs/SUPPA2.yaml
micromamba env create -f workflows/02_as_calling/envs/spladder.yaml
```

## Directory Structure Setup

```bash
# Create project directory structure
mkdir -p project/{data,references,results}

# Data directories
mkdir -p project/data/{fastq,aligned,AS_output}

# Reference directories
mkdir -p project/references/{genome,annotation,indices}
```

## Configuration Templates

### Create Configuration Files

```bash
# Alignment workflow
cd workflows/01_alignment
cp config/config.yml config/my_project.yml

# AS calling workflow
cd workflows/02_as_calling
cp config/config.yml config/my_project.yml
```

Edit configuration files with your paths (see [Usage Guide](usage.md)).

## Troubleshooting Installation

### Conda Issues

**Problem**: Slow environment solving
```
Solving environment: failed with initial frozen solve. Retrying with flexible solve.
```
**Solution**: Use micromamba or mamba instead of conda
```bash
# Micromamba is fastest
micromamba create -c conda-forge -c bioconda -n snakemake snakemake
```

**Problem**: Channel priority conflicts
```
Error: Incompatible packages
```
**Solution**: Set channel priority
```bash
conda config --set channel_priority strict
```

### STAR Index Issues

**Problem**: Out of memory during indexing
```
Error: Not enough memory
```
**Solution**: Use `--limitGenomeGenerateRAM` parameter
```bash
STAR --runMode genomeGenerate \
     --limitGenomeGenerateRAM 31000000000 \
     ...
```

### MAJIQ Installation Issues

**Problem**: MAJIQ installation fails
```
Error: Failed building wheel for majiq
```
**Solution**: Install dependencies first
```bash
micromamba install -c conda-forge htslib
export HTSLIB_INCLUDE_DIR=$CONDA_PREFIX/include
export HTSLIB_LIBRARY_DIR=$CONDA_PREFIX/lib
pip install git+https://bitbucket.org/biociphers/majiq_academic.git
```

### Disk Space Issues

**Problem**: Insufficient disk space
```
Error: No space left on device
```
**Solution**:
1. Clean conda cache: `micromamba clean --all` (or `conda clean --all`)
2. Remove unused environments: `micromamba env remove -n ENV_NAME`
3. Use external storage for data directories

## Verification Checklist

Before running the pipeline, verify:

- [ ] Snakemake ≥7.0.0 installed
- [ ] Reference genome downloaded and indexed
- [ ] GENCODE v34 GTF and GFF3 downloaded
- [ ] STAR index built
- [ ] Salmon index built
- [ ] SUPPA2 events generated
- [ ] MAJIQ license obtained
- [ ] Configuration files created
- [ ] Sufficient disk space available
- [ ] Test dry-run successful

## Next Steps

After successful installation:
1. Prepare your FASTQ files
2. Configure workflow parameters
3. Follow the [Usage Guide](usage.md)

## Support

If you encounter installation issues:
- Check [Troubleshooting](troubleshooting.md)
- Open an issue on GitHub
- Contact: jianguo.zhou@zmu.edu.cn
