#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash scripts/read_length.sh <coordinate-sorted.bam>" >&2
  exit 2
fi

bam_file="$1"
if [[ ! -f "$bam_file" ]]; then
  echo "BAM file does not exist: $bam_file" >&2
  exit 2
fi

samtools stats "$bam_file" | awk -F '\t' '
  $1 == "SN" && $2 == "maximum length:" {
    print $3
    found = 1
  }
  END {
    if (!found) {
      print "Unable to determine maximum read length" > "/dev/stderr"
      exit 1
    }
  }
'
