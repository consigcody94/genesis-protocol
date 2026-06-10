<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,25:1a0a2e,50:2d0a4e,75:0a2d4e,100:0d1117&height=250&section=header&text=THE%20GENESIS%20PROTOCOL&fontSize=60&fontColor=c9d1d9&animation=fadeIn&fontAlignY=30&desc=Computational%20Archaeology%20of%20the%20Masoretic%20Text&descAlignY=55&descSize=16&descColor=8b949e"/>

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![CI](https://img.shields.io/github/actions/workflow/status/consigcody94/genesis-protocol/ci.yml?style=flat-square&label=CI)](https://github.com/consigcody94/genesis-protocol/actions)
[![Entropy](https://img.shields.io/badge/Shannon_Entropy-7.7167_bits/byte-22c55e?style=flat-square)]()
[![Artifact](https://img.shields.io/badge/Binary_Artifact-742_KB-0891b2?style=flat-square)]()
[![Dashboard](https://img.shields.io/badge/Live_Dashboard-ACTIVE-f59e0b?style=flat-square)](https://consigcody94.github.io/genesis-protocol/)

<br/>

**What happens when you treat the Hebrew Bible not as literature, but as compiled machine code?**

A Base-22 transcoding of the complete Masoretic Text yields a 742 KB binary artifact<br/>
with entropy indistinguishable from high-density executables.

<br/>

[Live Dashboard](https://consigcody94.github.io/genesis-protocol/) &ensp;&bull;&ensp; [Methodology](#methodology) &ensp;&bull;&ensp; [Findings](#findings) &ensp;&bull;&ensp; [Toolkit](#toolkit) &ensp;&bull;&ensp; [Quick Start](#quick-start)

</div>

<br/>

> *"Turning the text... for everything is in it."* &mdash; Pirke Avot 5:22

<br/>

## The Hypothesis

Traditional "Bible Code" research uses Equidistant Letter Sequences (ELS), which are statistically fragile and prone to confirmation bias. The Genesis Protocol takes a fundamentally different approach:

**Treat the 22-letter Hebrew alphabet as a Base-22 numeral system and transcode the entire Tanakh into binary.**

The resulting artifact is not random noise. It is not natural language. Its information-theoretic signature falls squarely in the range of **compiled executable code**.

<br/>

## Methodology

### Step 1 &mdash; Lossless Extraction

The Hebrew alphabet (Aleph through Tav) maps to digits 0&ndash;21:

```
  (Aleph) = 0x00    (Bet) = 0x01    ...    (Tav) = 0x15
```

All vowels, cantillation marks, and punctuation are stripped. Every consonant in the Masoretic canon &mdash; from Genesis 1:1 through II Chronicles &mdash; is transcoded into a contiguous binary stream. The five final (sofit) letterforms fold into their base letters, so all 1,206,309 consonants are encoded.

**Encoding**: 13 Hebrew letters are packed per 64-bit word (22^13 < 2^64), producing a lossless, byte-aligned binary.

> **v1.1 encoder fix**: the original v1.0 extraction silently dropped final-form letters (ך ם ן ף ץ) &mdash; roughly 4% of the canon &mdash; making it lossy. The artifact, and every number below, has been regenerated with the corrected encoder. Several v1.0 "signatures" did not survive the fix; see the findings.

### Step 2 &mdash; Information-Theoretic Analysis

Shannon entropy measures information density on a scale of 0&ndash;8 bits/byte:

| Data Type | Entropy (bits/byte) | Interpretation |
|:--|:--:|:--|
| English plaintext | ~4.2 | Low-density, redundant |
| Hebrew plaintext | ~4.4 | Low-density, redundant |
| **Genesis Protocol binary** | **7.7167** | **High-density, structured** |
| Compressed archives (gzip) | 7.8&ndash;8.0 | Near-maximum density |
| True random noise | 8.0 | Maximum entropy |
| Compiled executables (ELF/PE) | 6.5&ndash;7.5 | High-density, structured |

The artifact's entropy (7.7167) is far above any natural language &mdash; but the null-hypothesis controls below show this is a property of the Base-22 *packing*, not of the text itself.

### Step 3 &mdash; Architecture Forensics

The `arch_detective.py` tool analyzes byte-level alignment, opcode distribution, and instruction encoding patterns to identify potential instruction set architectures (ISAs) in the binary.

### Step 4 &mdash; Execution

A custom RISC-V emulator (`genesis_runner.py`) attempts to execute instruction blocks mined from the artifact, recording register states, memory operations, and control flow.

<br/>

## Findings

Each finding is now paired with its null-hypothesis test (`null_hypothesis.py`). The key control is **shuffled Torah**: the exact same letters, randomly permuted, packed by the exact same encoder. Any signal that survives shuffling belongs to the *encoding*, not the *text*.

### Finding I &mdash; Entropy Anomaly &rarr; Encoding Artifact

The extracted binary measures **7.7167 bits/byte** &mdash; not natural language (4.4), not random noise (8.0).

**Control result**: shuffled Torah packs to **7.7169** and uniform random Base-22 digits pack to **7.7285** &mdash; statistically identical. The deficit below 8.0 is structural: 13 Base-22 digits occupy only ~58.1 of each 64-bit word, so the first byte of every 8-byte block is confined to values 0&ndash;4. **The entropy signature is a property of the Base-22 packing, and would appear for any 22-symbol text.**

### Finding II &mdash; Embedded Signatures &rarr; Did Not Replicate

The v1.0 binary appeared to contain ASCII signatures (**IPv6**, and a tight **DNA / CODE / NETWORK** cluster). After the v1.1 encoder fix, **none of these strings appear in the corrected binary**. Monte Carlo scans of shuffled-Torah control binaries produce keyword hits at the same chance rates as the real artifact (e.g. "AI" appears 13&times; in the real binary vs. a control mean of 21&times;). Short ASCII strings in 742 KB of dense data are expected by chance.

### Finding III &mdash; Cellular Automaton Behavior (Visual Only)

The first 8,192 bits of Genesis, used as a seed for a **Wolfram Rule 30** cellular automaton, produce a sustained, non-collapsing pattern with high visual complexity. No quantitative complexity comparison against random seeds has been run yet &mdash; this remains an open question.

### Finding IV &mdash; RISC-V Alignment &rarr; Encoding Artifact

13.8% of 32-bit words in the artifact carry a valid RV32I opcode in their low 7 bits, above the 8.6% chance rate (11 valid opcodes / 128).

**Control result**: shuffled Torah scores **13.6%** &mdash; the same elevation. Pure random bytes score 8.5%. The elevation comes from the packing's biased byte distribution, not from meaningful instruction encoding.

### Finding V &mdash; Execution Results (Mechanical Demonstration)

The Genesis Runner emulator executed the longest mined instruction chain from the corrected binary (5 instructions at offset `0x15210`): three LOADs, one ADD, and `LUI x8, 0x739DD000`, leaving register `x8` = **1,939,722,240**. This demonstrates the toolchain end-to-end; given Finding IV, mined "functions" are expected to occur by chance.

<br/>

## Toolkit

The complete analysis pipeline is open source and reproducible:

| Tool | Purpose | Input | Output |
|:--|:--|:--|:--|
| `download_data.py` | Fetch Masoretic text from Sefaria | &mdash; | `data/*.json` |
| `master_command_64.py` | Base-22 binary extraction | Hebrew text | `tanakh_full.bin` |
| `arch_detective.py` | ISA forensics & alignment analysis | Binary | Architecture report |
| `divine_disassembler.py` | RISC-V disassembly | Binary | `genesis.asm` |
| `deep_decoder.py` | Pattern & signature scanning | Binary | Anomaly report |
| `genesis_runner.py` | RISC-V emulation & execution | Assembly | Register states |
| `eternity_vm.py` | Cellular automaton simulation | Binary seed | Grid evolution |
| `entropy_lab.py` | Shannon entropy analysis | Binary | Entropy metrics |
| `function_miner.py` | Code block extraction | Binary | Function boundaries |
| `null_hypothesis.py` | Control experiments (shuffled/random corpora) | Binary + corpus | `null_hypothesis_report.txt` |

### Supporting Modules

| Module | Purpose |
|:--|:--|
| `torah_loader.py` | Loads all 39 canonical books in order |
| `text_processor.py` | Hebrew normalization (strip vowels, cantillation) |
| `gematria.py` | Numerical value computation (Standard, Ordinal, Reduced) |
| `els_search.py` | Equidistant Letter Sequence finder |
| `ciphers.py` | Atbash & Albam cipher tools |
| `main.py` | Interactive CLI workbench |

<br/>

## Quick Start

```bash
# Clone the repository
git clone https://github.com/consigcody94/genesis-protocol.git
cd genesis-protocol

# Download the Masoretic text corpus (39 books from Sefaria)
python download_data.py

# Run the Base-22 extraction
python master_command_64.py

# Analyze the binary artifact
python arch_detective.py
python entropy_lab.py

# Disassemble and execute
python divine_disassembler.py
python genesis_runner.py

# Run the null-hypothesis controls (the most important step)
python null_hypothesis.py

# Run the test suite
python -m unittest discover -s tests -t .

# Launch the live dashboard
# Open index.html in any browser, or visit:
# https://consigcody94.github.io/genesis-protocol/
```

**Requirements**: Python 3.9+ (standard library only &mdash; no external dependencies)

<br/>

## Live Dashboard

The interactive forensic dashboard visualizes the binary artifact in real-time:

- **Wolfram Rule 30** cellular automaton seeded with Genesis bits
- **String stream** showing decoded ASCII patterns
- **Entropy metrics** and artifact statistics
- **Anomaly highlighting** for identified signatures

**[Launch Dashboard](https://consigcody94.github.io/genesis-protocol/)**

<br/>

## Open Questions

Status after the v1.1 control experiments (`python null_hypothesis.py`, seeded and reproducible):

| Question | Status | Result |
|:--|:--|:--|
| Is the entropy significant vs. control texts? | **Tested** | No &mdash; shuffled Torah packs to identical entropy (7.7169 vs 7.7167) |
| How many short ASCII strings appear by chance in 742 KB? | **Tested** | Real keyword hits fall within Monte Carlo control ranges |
| Does the RISC-V alignment exceed random expectation? | **Tested** | It exceeds *random bytes* but matches *shuffled Torah* &mdash; an encoding artifact |
| Does the extraction method (Base-22) bias toward code-like entropy? | **Confirmed** | Yes &mdash; 13 digits fill only ~58 of 64 bits, capping any packed text below 8.0 |
| Are Rule 30 patterns from Genesis atypical? | Visual only | Still open &mdash; needs quantitative complexity metrics against random seeds |

Rigorous peer review from information theorists, computational linguists, and cryptographers is actively invited &mdash; the controls above are a starting point, not the final word.

<br/>

## Repository Structure

```
genesis-protocol/
  data/                     39 JSON books (Masoretic text from Sefaria)
  tests/                     Unit & regression tests (unittest)
  .github/workflows/ci.yml   CI: tests + full pipeline smoke run
  tanakh_full.bin            742 KB binary artifact (extracted)
  genesis.asm                RISC-V disassembly output
  null_hypothesis.py         Control experiments (the science)
  null_hypothesis_report.txt Latest control-run report
  index.html                 Live forensic dashboard
  genesis_data.js            Dashboard data layer
  genesis_protocol_core.json Core metadata
  master_command_64.py       Base-22 extraction engine
  arch_detective.py          ISA forensics
  divine_disassembler.py     RISC-V disassembler
  genesis_runner.py          RISC-V emulator
  deep_decoder.py            Pattern scanner
  eternity_vm.py             Cellular automaton
  entropy_lab.py             Entropy analysis
  main.py                    Interactive CLI
  torah_loader.py            Corpus loader
  text_processor.py          Hebrew normalization
  gematria.py                Numerical values
  els_search.py              ELS finder
  ciphers.py                 Atbash/Albam ciphers
```

<br/>

## Citation

If you use this toolkit or methodology in research:

```
@software{genesis_protocol,
  title  = {The Genesis Protocol: Computational Archaeology of the Masoretic Text},
  author = {Churchwell, Cody},
  year   = {2025},
  url    = {https://github.com/consigcody94/genesis-protocol}
}
```

<br/>

## License

[MIT License](LICENSE) &mdash; Open source. Fork it, verify it, challenge it.

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,25:1a0a2e,50:2d0a4e,75:0a2d4e,100:0d1117&height=100&section=footer"/>

<sub>
An open-source investigation into the information-theoretic properties of ancient Hebrew text.<br/>
Independent verification and rigorous critique are not just welcome &mdash; they are the point.
</sub>

</div>
