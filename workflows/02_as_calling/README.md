# Alternative Splicing Detection Workflow

This workflow detects alternative splicing events using four complementary algorithms: rMATS, MAJIQ, SUPPA2, and SplAdder.

## Overview

The AS calling workflow integrates four state-of-the-art tools, each with unique strengths:

- **rMATS**: Statistical framework for differential splicing
- **MAJIQ**: Local splicing variation (LSV) quantification
- **SUPPA2**: Fast event-based PSI calculation
- **SplAdder**: Graph-based splicing event detection

## Input Requirements

### Prerequisites
- **Aligned BAM files** from workflow 01_alignment
- BAM files must be:
  - Coordinate-sorted
  - Indexed (.bai files present)
  - Contain splice junction information

### Reference Files
- **GTF Annotation**: GENCODE v34
- **GFF3 Annotation**: GENCODE v34 (for MAJIQ)
- **Genome FASTA**: GRCh38 primary assembly
- **Salmon Index**: GENCODE v34 transcripts (for SUPPA2)
- **SUPPA2 Events**: Pre-generated .ioe file
- **MAJIQ License**: Academic license file

## Configuration

Edit `config/config.yml`:

```yaml
read_len: 150  # Maximum read length

raw_DIR: /path/to/fastq

bam_DIR: /path/to/aligned

workdir: /path/to/AS_output

MAJIQ_license: /path/to/majiq_license_academic_official.lic

suppa2_events: /path/to/gencode.v34.events.ioe

SALMON_INDEX: /path/to/gencode.v34.transcripts.salmon.index

strandness: fr-firststrand

ref: /path/to/gencode.v34.annotation.gtf

ref_fa: /path/to/GRCh38.primary_assembly.genome.fa

GFF: /path/to/gencode.v34.annotation.gff3
```

## Usage

### 1. Prepare Configuration

```bash
cd workflows/02_as_calling
cp config/config.yml config/my_config.yml
# Edit my_config.yml
```

### 2. Check Read Length

```bash
# Run read length check script
bash scripts/read_length.sh /path/to/bam/sample.bam

# Update read_len in config.yml with maximum value
```

### 3. Dry Run

```bash
snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 1 --use-conda --dry-run
```

### 4. Run Workflow

```bash
# Set temporary directory (important for large datasets)
export TMPDIR=/path/to/large/tmp

# Run workflow
nohup snakemake -s Snakefile --configfile config/my_config.yml \
  --cores 40 --use-conda --rerun-incomplete --retries 3 \
  --keep-going > as_calling.log 2>&1 &

# Save process ID
echo $! > run.pid
```

## Output Structure

```
AS_output/
└── {sample}/
    ├── rmats/
    │   ├── A3SS.MATS.JC.txt
    │   ├── A5SS.MATS.JC.txt
    │   ├── MXE.MATS.JC.txt
    │   ├── RI.MATS.JC.txt
    │   └── SE.MATS.JC.txt
    ├── majiq/
    │   ├── {sample}_Aligned.sortedByCoord.out.majiq
    │   ├── {sample}_Aligned.sortedByCoord.out.sj
    │   ├── splicegraph.sql
    │   ├── {sample}.psi.tsv
    │   ├── {sample}.psi.voila
    │   ├── {sample}.voila.tsv
    │   └── modulized/
    ├── suppa2/
    │   └── {sample}_event.psi
    └── spladder/
        ├── genes_graph_conf0.pickle
        ├── merge_graphs_exon_skip_C0.confirmed.txt.gz
        ├── merge_graphs_intron_retention_C0.confirmed.txt.gz
        ├── merge_graphs_alt_3prime_C0.confirmed.txt.gz
        ├── merge_graphs_alt_5prime_C0.confirmed.txt.gz
        └── merge_graphs_mutex_exons_C0.confirmed.txt.gz
```

## Algorithm Details

### rMATS

**Purpose**: Detect differential splicing between conditions

**Parameters**:
```bash
rmats.py \
  --b1 {bam_list} \
  --gtf {annotation} \
  --readLength {read_len} \
  --nthread 30 \
  -t paired \
  --cstat 0.0001 \
  --variable-read-length
```

**Output**: 5 event types (SE, A3SS, A5SS, MXE, RI)

**Key Metrics**:
- IncLevel: Inclusion level (PSI)
- FDR: False discovery rate
- IncLevelDifference: ΔPSI

---

### MAJIQ

**Purpose**: Quantify local splicing variations (LSVs)

**Workflow**:
1. **Build**: Construct splice graph
   ```bash
   majiq build {gff} -c {config} -j 30 --minreads 10
   ```

2. **Quantify**: Calculate PSI values
   ```bash
   majiq psi {majiq_file} -n {sample}
   ```

3. **Visualize**: Generate TSV output
   ```bash
   voila tsv -f {output} {sql} {voila}
   ```

**Output**: LSV-level PSI values

---

### SUPPA2

**Purpose**: Fast transcript-based PSI calculation

**Workflow**:
1. **Quantify Transcripts**: Salmon quantification
   ```bash
   salmon quant -i {index} -l ISF --gcBias \
     -1 {R1} -2 {R2} -p 15
   ```

2. **Calculate PSI**: Event-level PSI
   ```bash
   suppa.py psiPerEvent -i {events} -f 1 -e {tpm}
   ```

**Output**: Event-level PSI (7 event types)

---

### SplAdder

**Purpose**: Graph-based comprehensive event detection

**Parameters**:
```bash
spladder build \
  --bams {bam} \
  --annotation {gtf} \
  --outdir {output} \
  --parallel 10 \
  -v
```

**Output**: 5 event types with confidence scores

## Performance

### Resource Requirements

| Tool | CPU | Memory | Time (per sample) |
|------|-----|--------|-------------------|
| rMATS | 30 cores | 16 GB | 1-2 hours |
| MAJIQ | 30 cores | 8 GB | 30-60 min |
| SUPPA2 | 15 cores | 4 GB | 20-40 min |
| SplAdder | 10 cores | 8 GB | 1-2 hours |

### Optimization

1. **Parallel Samples**: Snakemake automatically parallelizes across samples
2. **Temporary Storage**: Set `TMPDIR` to fast storage for rMATS
3. **Memory**: Ensure sufficient RAM for large BAM files

## Troubleshooting

### rMATS Issues

**Problem**: Variable read length error
```
Error: Read length inconsistency
```
**Solution**: Use `--variable-read-length` flag (already included)

**Problem**: Out of disk space
```
Error: No space left on device
```
**Solution**: Set `TMPDIR` to larger partition

---

### MAJIQ Issues

**Problem**: License error
```
Error: License file not found
```
**Solution**: Obtain academic license from MAJIQ website and update config

**Problem**: GFF3 format error
```
Error: Invalid GFF3 format
```
**Solution**: Ensure using GENCODE GFF3 (not GTF)

---

### SUPPA2 Issues

**Problem**: Salmon index mismatch
```
Error: Index version mismatch
```
**Solution**: Rebuild Salmon index with same version

**Problem**: Missing events file
```
Error: .ioe file not found
```
**Solution**: Generate events file:
```bash
suppa.py generateEvents -i {gtf} -o {output} -f ioe
```

---

### SplAdder Issues

**Problem**: Memory error
```
Error: MemoryError
```
**Solution**: Reduce `--parallel` parameter or increase RAM

## Quality Metrics

After completion, check:

1. **Event Counts**: Each tool should detect thousands of events
   ```bash
   # rMATS
   wc -l AS_output/*/rmats/SE.MATS.JC.txt

   # MAJIQ
   wc -l AS_output/*/majiq/*.voila.tsv

   # SUPPA2
   wc -l AS_output/*/suppa2/*_event.psi
   ```

2. **PSI Distribution**: PSI values should range 0-1

3. **Completion**: All expected output files present

## Next Steps

After AS detection:
- Quality filtering (PSI > 0.1, coverage > 33%)
- Consensus calling (2-out-of-4 framework)
- Differential splicing analysis
- Integration with clinical data

## References

- **rMATS**: Shen et al., PNAS 2014
- **MAJIQ**: Vaquero-Garcia et al., eLife 2016
- **SUPPA2**: Trincado et al., Genome Biology 2018
- **SplAdder**: Kahles et al., Genome Biology 2016
- **Salmon**: Patro et al., Nature Methods 2017
