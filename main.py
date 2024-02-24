#!/usr/bin/env python3

import re
import sys
import json
import requests

# config
TIMEOUT = 30 # seconds
HOST_URI = "https://web.expasy.org/cgi-bin/protparam/protparam"

# match patterns
molecular_weight = r"<B>Molecular weight:</B> (.*)"
theoretical_pI = r"<B>Theoretical pI:</B> (.*)"
half_life = r"The estimated half-life is: (.*) \("
instability_index = r"The instability index \(II\) is computed to be (.*)"
stability_bool = r"This classifies the protein as (.*)\."
aliphatic_index = r"<B>Aliphatic index:</B> (.*)"
GRAVY = r"<B>Grand average of hydropathicity \(GRAVY\):</B> (.*)"


def compute_protparams(sequence):
    try:
        res = requests.post(HOST_URI, data={"sequence": sequence}, timeout=TIMEOUT)

        results = {
            "molecular_weight": float(re.search(molecular_weight, res.text).group(1)),
            "theoretical_pI": float(re.search(theoretical_pI, res.text).group(1)),
            "half_life": re.search(half_life, res.text).group(1),
            "instability_index": float(re.search(instability_index, res.text).group(1)),
            "stability_bool": re.search(stability_bool, res.text).group(1) == "stable",
            "aliphatic_index": float(re.search(aliphatic_index, res.text).group(1)),
            "GRAVY": float(re.search(GRAVY, res.text).group(1)),
        }

    # TODO: better exception handling
    except Exception as e: 
        print("Failed for sequence: ", sequence_file)

        results = {
            "molecular_weight": 0.0,
            "theoretical_pI": 0.0,
            "half_life": "",
            "instability_index": 0.0,
            "stability_bool": None,
            "aliphatic_index": 0.0,
            "GRAVY": 0.0,
        }

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <sequence>", file=sys.stderr)
        sys.exit(1)

    sequence = sys.argv[1]
    results = compute_protparams(sequence)

    print(json.dumps(results))
