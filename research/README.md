# Research notes

This directory contains the reasoning behind the experiments in the root [README](../README.md).

The main result is the **key-free watermark indicator** described in [key-free-twins.md](key-free-twins.md): matched marked/unmarked generations contain enough statistical structure to classify most held-out prompt groups without using the detector keys.

| File | Focus |
|---|---|
| [key-free-twins.md](key-free-twins.md) | Key-free watermark indication from matched generations; current best 10/12–11/12 at prompt grain |
| [how-synthid-works.md](how-synthid-works.md) | How the public SynthID-Text reference implementation hashes, samples, and scores |
| [invertibility.md](invertibility.md) | Why the key-free result is not key recovery |
| [claude.md](claude.md) | Anthropic's announced text marking and what can actually be measured |
| [paired-corpus.md](paired-corpus.md) | Before/after protocol for a future real-world key-free test |
| [dipper-local.md](dipper-local.md) | Why the official 11B DIPPER checkpoint is not part of the current setup |
| [HOW-TO.md](../HOW-TO.md) | Installation and practical commands |

The conceptual split is simple:

**known keys → `score`**  
**unknown keys + paired evidence → `blind` / `indicate`**
