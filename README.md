# The Emergence of Reality and Derived Specular Bit Architecture (SBA)

This repository collects the cosmological foundation **The Emergence of Reality** and the derived **Specular Bit Architecture (SBA)**. SBA is presented as a direct derivation of the cosmological model; a single Python verification tool is provided as the only supplementary artifact and generates all derived data (CSV, TXT, JSON) on demand.

---

## Repository structure

- `README.md` — this file.
- `theory/`  
  - `The_Emergence_of_Reality.pdf` — main cosmological manuscript (conceptual root). **[DOI: 10.5281/zenodo.19071941](https://doi.org/10.5281/zenodo.19071941)**
  - `The_Emergence_of_Reality.tex` — (optional) LaTeX source.
- `sba/`  
  - `SBA_Framework.pdf` — SBA derivation and formal framework. **[DOI: 10.5281/zenodo.19071172](https://doi.org/10.5281/zenodo.19071172)**
  - `SBA_Framework.tex` — (optional) LaTeX source.
- `code/`  
  - `SBA_Verification_Tool_v2.py` — **only** supplementary artifact. Running this script produces the canonical patterns CSV, the critical-pairs CSV, a human-readable verification report, and a compact JSON summary.
- `LICENSE` — license file(s) for code and manuscripts (MIT).

---

## Logical dependency

**Theory → SBA → Code**

The cosmological theory ("The Emergence of Reality") is the conceptual foundation. The SBA is derived from that theory. The Python tool implements the verification and reproduces the enumerations and tables used in the SBA manuscript.

---

## How to run the verification tool

**Requirements**

- Python 3.8 or newer (standard library only).

**Quick run**

```bash
cd code
python3 SBA_Verification_Tool_v2.py

