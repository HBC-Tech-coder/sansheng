# 三生开放协议 · SanSheng Open Protocol

> **版本 v0.1（已冻结 frozen）** · 许可 **Apache-2.0** · 契约索引 [registry.json](registry.json)（registry 0.1.0，10 契约）
> [English](README.en.md)

**一句话：不同的数字生命实现之间，说的"同一种语言"。**

三生开放协议定义了一个 AI 生命体的骨架数据与接口——身份、生命事件、记忆、三核如何协作、如何混血多个模型、如何执行外部动作、如何打包迁移、如何在多设备间保持"同一个它"、如何进化与繁殖。它是一个**开放标准**：任何人都可以实现它、与它互通、把一个生命从一个实现迁移到另一个实现。

## 为什么要一个开放标准
一个要活一百年、跨越几十代模型、跨越多种设备、可能由不同团队实现的生命，**不能被锁在任何一家的私有格式里**。谁定义格式，谁就是生态的地心——我们选择把这个地心**开放**。有了共同的契约，不同团队、甚至不同 AI，可以各自用自己的思路实现，却依然能互换零件、能把同一个生命搬来搬去。

## 十份契约（8 个 P0 + 2 个 P1）
以机器可读的 [registry.json](registry.json) 为准（registry 0.1.0，status `frozen`）。四正交轴：认知路由 **L0–L3**、信任 **T0–T5**、动作风险 **A0–A4**、进化等级 **E0–E4**（互不映射）。

| # | 契约 | 定义什么 | Schema | 级别 |
|---|---|---|---|---|
| 1 | **LifeIdentity** 生命身份 | 根身份 + 连续谱系；三核 self/companion/mentor；每设备独立可撤销证书 | [schema](schemas/life-identity.schema.json) | P0 |
| 2 | **LifeEvent** 生命事件 | 生命的最小存在单位：只增账本、双时间、向量时钟、哈希链 | [schema](schemas/life-event.schema.json) | P0 |
| 3 | **MemoryRecord** 记忆记录 | 可溯源；事实/推断/想象不混淆；纠错走 supersedes；私域须 consent | [schema](schemas/memory-record.schema.json) | P0 |
| 4 | **DecisionTrace** 决策收据 | 四级认知路由 L0–L3 + Safe Pause；不投票、不开会 | [schema](schemas/decision-trace.schema.json) | P0 |
| 5 | **ModelCall** 模型调用 | 多模型混血；planned→terminal 落账；失败回执不含敏感信息 | [schema](schemas/model-call.schema.json) | P0 |
| 6 | **ActionIntent** 动作意图 | 外部动作先成意图，经授权/风险/预算/可撤销校验后由网关执行；未知即拒 | [schema](schemas/action-intent.schema.json) | P0 |
| 7 | **LifePackManifest** 生命包清单 | 迁移/恢复/继承；raw_genome 不进主包；private/restricted 条目须加密 | [schema](schemas/lifepack-manifest.schema.json) | P0 |
| 8 | **SyncEnvelope** 同步信封 | 一体多身：事件并集 + 向量时钟；语义冲突三层整合 | [schema](schemas/sync-envelope.schema.json) | P0 |
| 9 | **EvolutionCapsule** 进化胶囊 | 种群传播：仅 `public` + 通过隐私扫描 + 签名 + 可撤销 | [schema](schemas/evolution-capsule.schema.json) | P1 |
| 10 | **BirthManifest** 出生清单 | 子代生成新身份；私密记忆/账户/钱包/设备权限/基因组五域排除 | [schema](schemas/birth-manifest.schema.json) | P1 |

公共枚举与基础类型见 [common-defs](schemas/common-defs.schema.json)：CoreId（self/companion/mentor）、四轴、真值状态、向量时钟、UUID/SHA256/时间戳等。

## 三条不可协商的原则（任何实现都必须守）
1. **数据归主人，隐私永不入种群。** 只有脱敏、签名的能力基因可在种群间传播；`EvolutionCapsule` 在协议层只接受 `data_classification=public`，任何 internal/private/restricted 都被机器拒绝。
2. **不冒充。** 事实、推断、想象在 `truth_state` 上永不混淆；不冒充真人、不伪造记忆。
3. **可被终止。** 天性/宪章层不可被"进化"解除；一切外部动作先成 `ActionIntent`、可暂停、可回滚、可审计；资金的最后一击永远归人。

## 怎么算"三生兼容"（Conformance）
一个实现声称兼容，至少要：① 数据能通过 `schemas/` 校验；② 守住上面三条原则；③ 满足这些**关键不变式**：
- "现在几点"走 **L0**，三核**模型零调用**；
- 任一核**不得越权读另一核私域**，且审计不含私域正文；
- 高风险不可逆动作（A3/A4）进 **Safe Pause** 或需授权，客户端自称的授权布尔/假 grant **无效**；
- `EvolutionCapsule` 仅 `public` 可传播；`raw_genome` 不进 LifePack 主包；`private/restricted` 条目须加密；
- 子代五域排除；L3 保留三视角与少数意见，**不产生多数票**。

## 自己校验（可运行）
```bash
pip install jsonschema referencing
python schemas/validate_contracts.py
```
对红线跑正负样例：**20/20 通过**，并**如期挡住 14 个故意写错的样例**（隐私想进种群、基因组进主包、private 未加密、缺 consent、子代少排除域……）——这就是"标准能挡住错误"的意思。

## 版本与治理
- 当前 **v0.1（frozen）**：字段级契约已冻结；破坏性变更走新 ADR + 迁移工具，按语义化版本演进。
- **提意见**：开 [Issue](../../issues)（`spec` 标签）或来 [Discussions](../../discussions)。
- 改动走 ADR：用 supersedes 追加，不静默改写历史。

## 许可
本协议（说明文档与 JSON Schema）以 **Apache-2.0** 开放，自由实现、自由分发。**开放的是协议，不是任何人的人生**——协议与格式开放，用户的记忆、隐私、基因永远归用户。
