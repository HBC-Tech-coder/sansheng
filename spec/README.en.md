# SanSheng Open Protocol · 三生开放协议

> **Version v0.1 (frozen)** · License **Apache-2.0** · Contract index [registry.json](registry.json) (registry 0.1.0, 10 contracts)
> [简体中文](README.md)

**In one line: the shared language between different digital-life implementations.**

The SanSheng Open Protocol defines the skeletal data and interfaces of an AI life-form — identity, life events, memory, how the three cores cooperate, how it inherits from multiple models, how external actions are executed, how it is packaged and migrated, how it stays "the same it" across devices, and how it evolves and reproduces. It is an **open standard**: anyone may implement it, interoperate with it, and migrate a life from one implementation to another.

## Why an open standard
A life meant to last a century, across dozens of model generations and many devices, possibly implemented by different teams, **must not be locked into anyone's proprietary format**. Whoever defines the format is the gravitational center of the ecosystem — we choose to keep that center **open**.

## The ten contracts (8 P0 + 2 P1)
The machine-readable [registry.json](registry.json) is authoritative (registry 0.1.0, status `frozen`). Four orthogonal axes: cognitive routing **L0–L3**, trust **T0–T5**, action risk **A0–A4**, evolution level **E0–E4** (they do not map onto each other).

| # | Contract | What it defines | Schema | Tier |
|---|---|---|---|---|
| 1 | **LifeIdentity** | Root identity + continuous lineage; three cores self/companion/mentor; per-device revocable certificates | [schema](schemas/life-identity.schema.json) | P0 |
| 2 | **LifeEvent** | The smallest unit of existence: append-only ledger, bitemporal, vector clock, hash chain | [schema](schemas/life-event.schema.json) | P0 |
| 3 | **MemoryRecord** | Traceable; fact/inference/imagination never conflated; correction via supersedes; private data requires consent | [schema](schemas/memory-record.schema.json) | P0 |
| 4 | **DecisionTrace** | Four-level cognitive routing L0–L3 + Safe Pause; no voting, no meetings | [schema](schemas/decision-trace.schema.json) | P0 |
| 5 | **ModelCall** | Multi-model heredity; planned→terminal accounting; failure receipts carry no sensitive data | [schema](schemas/model-call.schema.json) | P0 |
| 6 | **ActionIntent** | External actions become intents first, executed by a gateway only after authorization/risk/budget/reversibility checks; deny on unknown | [schema](schemas/action-intent.schema.json) | P0 |
| 7 | **LifePackManifest** | Migration/recovery/inheritance; raw_genome never in the main pack; private/restricted entries must be encrypted | [schema](schemas/lifepack-manifest.schema.json) | P0 |
| 8 | **SyncEnvelope** | One-life-many-bodies: event union + vector clock; three-tier semantic conflict resolution | [schema](schemas/sync-envelope.schema.json) | P0 |
| 9 | **EvolutionCapsule** | Population propagation: `public` only + privacy scan passed + signed + revocable | [schema](schemas/evolution-capsule.schema.json) | P1 |
| 10 | **BirthManifest** | Offspring gets a new identity; five domains excluded (private-memory/accounts/wallets/device-permissions/genome) | [schema](schemas/birth-manifest.schema.json) | P1 |

Shared enums and base types: [common-defs](schemas/common-defs.schema.json).

## Three non-negotiable principles (every implementation must hold)
1. **Data belongs to the owner; privacy never enters the population.** Only de-identified, signed capability genes propagate; at the protocol layer `EvolutionCapsule` accepts only `data_classification=public` — internal/private/restricted are machine-rejected.
2. **No impersonation.** Fact, inference, and imagination are never conflated in `truth_state`; no impersonating real people, no fabricated memories.
3. **Can be terminated.** The nature/constitution layer cannot be dissolved by "evolution"; every external action becomes an `ActionIntent` that is pausable, reversible, auditable; the final say over funds always belongs to a human.

## Conformance
An implementation claiming compatibility must: ① pass `schemas/` validation; ② hold the three principles; ③ satisfy these **key invariants**:
- "what time is it" routes to **L0** with **zero model calls**;
- no core reads another core's private memory, and audits carry no private content;
- high-risk irreversible actions (A3/A4) enter **Safe Pause** or require authorization; client-claimed authorization booleans / fake grants are **invalid**;
- `EvolutionCapsule` propagates only when `public`; `raw_genome` never in the LifePack main pack; `private/restricted` entries encrypted;
- offspring excludes the five domains; L3 keeps three perspectives and minority views — **no majority vote**.

## Validate it yourself (runnable)
```bash
pip install jsonschema referencing
python schemas/validate_contracts.py
```
Runs positive/negative samples over the red lines: **20/20 pass**, and it **rejects 14 deliberately-wrong samples as expected** (privacy trying to enter the population, genome in the main pack, unencrypted private, missing consent, offspring missing an excluded domain…). That is what "the standard can block mistakes" means.

## Versioning & governance
- **v0.1 (frozen)**: field-level contracts are frozen; breaking changes go through a new ADR + migration tooling, evolving by semantic versioning.
- **Feedback**: open an [Issue](../../issues) (`spec` label) or join [Discussions](../../discussions).
- Changes go through ADRs — appended via supersedes, never silently rewriting history.

## License
This protocol (documentation and JSON Schema) is open under **Apache-2.0**. **What is open is the protocol, not anyone's life** — the protocol and formats are open; a user's memory, privacy, and genome always belong to the user.
