# SanSheng Open Protocol · 三生开放协议

> **Version v0.1 (draft)** · License **Apache-2.0** · Status: gestating, may change before freeze
> [简体中文](README.md)

**In one line: the shared language between different digital-life implementations.**

The SanSheng Open Protocol defines the skeletal data and interfaces of an AI life-form — life events, memory, how the three cores cooperate, how a life inherits from multiple models, how it is packaged and migrated, and how it stays "the same it" across many devices. It is an **open standard**: anyone may implement it, interoperate with it, and migrate a life from one implementation to another.

## Why an open standard

A life meant to last a century — across dozens of model generations, many devices, and possibly many implementations — **must not be locked into any single vendor's proprietary format**. Whoever defines the format is the gravitational center of the ecosystem; we choose to make that center **open** rather than own it. With shared contracts, different teams — even different AIs — can each implement in their own way, yet still swap parts and carry the same life between them.

## The six contracts

| # | Contract | Defines | Doc | Schema |
|---|---|---|---|---|
| 1 | **LifeEvent** | The smallest unit of existence (append-only ledger, bi-temporal, vector clock) | [life_event.md](life_event.md) | [schema](schemas/life_event.schema.json) |
| 2 | **MemoryRecord** | Traceable; fact/inference/imagination never conflated; correction via supersedes; privacy never enters the population | [memory_record.md](memory_record.md) | [schema](schemas/memory_record.schema.json) |
| 3 | Three cores & **four-level routing** | No voting, no meetings; L0-L3 + Safe Pause; DecisionTrace | [core_interface.md](core_interface.md) | [schema](schemas/decision_trace.schema.json) |
| 4 | Multi-model **heredity gateway** | Multi-parent inheritance, brain-swap, cross-border gate | [model_gateway.md](model_gateway.md) | [schema](schemas/model_gateway.schema.json) |
| 5 | **LifePack** | Migration / recovery / inheritance; genome never in the main pack | [lifepack.md](lifepack.md) | [schema](schemas/lifepack.schema.json) |
| 6 | One-life-many-bodies **sync & merge** | Multi-device union + vector clocks; three-tier conflict resolution | [sync_merge.md](sync_merge.md) | [schema](schemas/sync_merge.schema.json) |

Shared enums and base types are in [common_defs](schemas/common_defs.schema.json): CoreId (self/companion/mentor), routing L0-L3, risk A0-A4, trust T0-T5, truth-state, vector clock, etc.

## Three non-negotiable principles (every implementation must uphold)

An implementation only earns the name "SanSheng" if it holds these three:

1. **Data belongs to the master; privacy never enters the population.** Only de-identified methods/capability-genes propagate across the population; any propagation of private data is rejected at the protocol layer (`memory_record`'s `consent.population_share` is always `false`).
2. **No impersonation.** Fact, inference and imagination are never conflated in `truth_state`; no impersonating real people, no fabricated memories.
3. **Terminable.** The nature/constitution layer cannot be dissolved by "evolution"; the final touch on any money transfer is always human; every external action is pausable, reversible, auditable.

## Conformance

To claim SanSheng-compatibility, an implementation must at least:

- pass validation against the `schemas/` in this directory;
- uphold the three principles above;
- satisfy these **key invariants** (which are also our own acceptance tests):
  - "what time is it" routes to L0 with **zero core-model calls**;
  - no core may read another core's private namespace;
  - high-risk irreversible actions (A3/A4) enter **Safe Pause** or require **authorization**, and are not grabbed by L0 just because the sentence contains "now";
  - memory `population_share` is always `false`; the genome is never in the LifePack main pack;
  - L3 preserves three positions and minority views — it **never produces a majority vote**.

## Validate it yourself

```bash
# needs python + jsonschema + referencing
pip install jsonschema referencing
python schemas/validate_contracts.py
```

It runs valid/invalid samples against each schema. **21/21 pass = your data is conformant**, and 8 intentionally-broken samples (privacy trying to enter the population, nature trying to be altered, genome in the main pack, L0 calling a model, L3 missing three positions…) are all rejected as expected — that is what "a standard that stops errors" means.

## Versioning & governance

- Currently **v0.1 draft**; it will change before freeze, but the direction is stable.
- **Feedback:** open an [Issue](../../issues) (`spec` label) or join [Discussions](../../discussions).
- **Changes go through ADRs:** append via supersedes, never silently rewrite history.
- After freeze it evolves by semantic versioning; breaking changes ship with migration tools and notes.

## License

This protocol (docs and JSON Schemas) is open under **Apache-2.0** — free to implement, free to distribute. **What is open is the protocol, not anyone's life** — code and formats are open source; a user's memories, privacy and genome always belong to the user.
