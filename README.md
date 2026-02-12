<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,25:1a0a2e,50:2d0a4e,75:0a2d4e,100:0d1117&height=250&section=header&text=THE%20GENESIS%20PROTOCOL&fontSize=60&fontColor=c9d1d9&animation=fadeIn&fontAlignY=30&desc=Computational%20Archaeology%20of%20the%20Masoretic%20Text&descAlignY=55&descSize=16&descColor=8b949e"/>

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Entropy](https://img.shields.io/badge/Shannon_Entropy-7.4995_bits/byte-22c55e?style=flat-square)]()
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

All vowels, cantillation marks, and punctuation are stripped. Every consonant in the Masoretic canon &mdash; from Genesis 1:1 through II Chronicles &mdash; is transcoded into a contiguous binary stream.

**Encoding**: 13 Hebrew letters are packed per 64-bit word (22^13 < 2^64), producing a lossless, byte-aligned binary.

### Step 2 &mdash; Information-Theoretic Analysis

Shannon entropy measures information density on a scale of 0&ndash;8 bits/byte:

| Data Type | Entropy (bits/byte) | Interpretation |
|:--|:--:|:--|
| English plaintext | ~4.2 | Low-density, redundant |
| Hebrew plaintext | ~4.4 | Low-density, redundant |
| **Genesis Protocol binary** | **7.4995** | **High-density, structured** |
| Compressed archives (gzip) | 7.8&ndash;8.0 | Near-maximum density |
| True random noise | 8.0 | Maximum entropy |
| Compiled executables (ELF/PE) | 6.5&ndash;7.5 | High-density, structured |

The artifact's entropy (7.4995) places it in the overlap zone between compiled code and compressed data &mdash; and well outside the range of any natural language.

### Step 3 &mdash; Architecture Forensics

The `arch_detective.py` tool analyzes byte-level alignment, opcode distribution, and instruction encoding patterns to identify potential instruction set architectures (ISAs) in the binary.

### Step 4 &mdash; Execution

A custom RISC-V emulator (`genesis_runner.py`) attempts to execute instruction blocks mined from the artifact, recording register states, memory operations, and control flow.

<br/>

## Findings

### Finding I &mdash; Entropy Anomaly

The extracted binary is **not** natural language entropy (4.4) and **not** random noise (8.0). It occupies a narrow band consistent with compiled, structured data. This is the foundational observation that motivates all subsequent analysis.

### Finding II &mdash; Embedded Signatures

Deep hex scanning (`deep_decoder.py`) identified ASCII-compatible signatures within the binary, including:

- **IPv6** &mdash; A 128-bit addressing protocol formalized in 1998
- **DNA**, **CODE**, **NETWORK** &mdash; Found in a statistically tight cluster (~150 bytes)

> **Note**: The statistical significance of finding short ASCII strings in a 742 KB binary requires careful null-hypothesis testing. See [Open Questions](#open-questions).

### Finding III &mdash; Cellular Automaton Behavior

The first 8,192 bits of Genesis, used as a seed for a **Wolfram Rule 30** cellular automaton, produce a sustained, non-collapsing pattern with high visual complexity.

### Finding IV &mdash; RISC-V Alignment

The binary exhibits 32-bit alignment patterns and opcode distribution consistent with RISC-V instruction encoding. The `divine_disassembler.py` tool produces valid RISC-V assembly from extracted blocks.

### Finding V &mdash; Execution Results

The Genesis Runner emulator executed a mined instruction block:
- Valid arithmetic operations performed
- Register `x26` loaded value **11,843,461,120,000** (`0x2B0F8000`)
- Control flow exhibited structured branching, not random jumps

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

# Launch the live dashboard
# Open index.html in any browser, or visit:
# https://consigcody94.github.io/genesis-protocol/
```

**Requirements**: Python 3.8+ (standard library only &mdash; no external dependencies)

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

This project raises questions that require further investigation:

| Question | Status | Approach Needed |
|:--|:--|:--|
| Is the entropy significant vs. control texts? | Untested | Compare English Bible, shuffled Torah, random Base-22 |
| How many short ASCII strings appear by chance in 742 KB? | Untested | Monte Carlo simulation on random binaries of same size |
| Does the RISC-V alignment exceed random expectation? | Partially tested | Statistical comparison against multiple ISA templates |
| Are Rule 30 patterns from Genesis atypical? | Visual only | Quantitative complexity metrics against random seeds |
| Does the extraction method (Base-22) bias toward code-like entropy? | Unknown | Test alternative base encodings (Base-20, Base-26, etc.) |

Rigorous peer review from information theorists, computational linguists, and cryptographers is actively invited.

<br/>

## Repository Structure

```
genesis-protocol/
  data/                     39 JSON books (Masoretic text from Sefaria)
  tanakh_full.bin            742 KB binary artifact (extracted)
  genesis.asm                RISC-V disassembly output
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

[MIT License](https://opensource.org/licenses/MIT) &mdash; Open source. Fork it, verify it, challenge it.

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,25:1a0a2e,50:2d0a4e,75:0a2d4e,100:0d1117&height=100&section=footer"/>

<sub>
An open-source investigation into the information-theoretic properties of ancient Hebrew text.<br/>
Independent verification and rigorous critique are not just welcome &mdash; they are the point.
</sub>

</div>
