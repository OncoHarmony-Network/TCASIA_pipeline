# Outputs

## Alignment

```text
{output_dir}/
├── clean_fastq/
├── qc/
│   ├── {sample}_fastp.html
│   └── {sample}_fastp.json
├── aligned/{sample}/
│   ├── {sample}_Aligned.out.bam
│   ├── {sample}_Aligned.sortedByCoord.out.bam
│   ├── {sample}_Aligned.sortedByCoord.out.bam.bai
│   └── {sample}_featureCounts.txt
└── logs/
```

## AS calling

```text
{output_dir}/
├── {sample}/
│   ├── rmats/
│   │   └── *.MATS.JC.txt
│   ├── majiq/
│   │   ├── {sample}.psi.tsv
│   │   ├── {sample}.psi.voila
│   │   ├── {sample}.voila.tsv
│   │   ├── splicegraph.sql
│   │   └── modulized/
│   ├── suppa2/
│   │   └── {sample}_event.psi
│   └── spladder/
├── work/
└── logs/
```

Caller-specific columns follow the official rMATS, MAJIQ/Voila, SUPPA2, and SplAdder formats.
