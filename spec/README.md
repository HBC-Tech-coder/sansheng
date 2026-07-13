# 三生开放协议 · SanSheng Open Protocol

> **版本 v0.1（草案）** · 许可 **Apache-2.0** · 状态：孕育中，冻结前可能变
> [English](README.en.md)

**一句话：不同的数字生命实现之间，说的"同一种语言"。**

三生开放协议定义了一个 AI 生命体的骨架数据与接口——生命事件、记忆、三核如何协作、如何混血多个模型、如何打包迁移、如何在多设备间保持"同一个它"。它是一个**开放标准**：任何人都可以实现它、与它互通、把一个生命从一个实现迁移到另一个实现。

## 为什么要一个开放标准

一个要活一百年、跨越几十代模型、跨越多种设备、可能由不同团队实现的生命，**不能被锁在任何一家的私有格式里**。谁定义格式，谁就是生态的地心——我们选择把这个地心**开放**，而不是独占。有了共同的契约，不同的团队、甚至不同的 AI，可以各自用自己的思路实现，却依然能互换零件、能把同一个生命搬来搬去。

## 六份契约

| # | 契约 | 定义什么 | 文件 | Schema |
|---|---|---|---|---|
| 1 | 生命事件 **LifeEvent** | 生命的最小存在单位（只增账本、双时间、向量时钟） | [life_event.md](life_event.md) | [schema](schemas/life_event.schema.json) |
| 2 | 记忆记录 **MemoryRecord** | 可溯源；事实/推断/想象不混淆；纠错走 supersedes；隐私永不入种群 | [memory_record.md](memory_record.md) | [schema](schemas/memory_record.schema.json) |
| 3 | 三核接口与**四级路由** | 不投票、不开会；L0-L3 + Safe Pause；决策收据 DecisionTrace | [core_interface.md](core_interface.md) | [schema](schemas/decision_trace.schema.json) |
| 4 | 多模型**混血网关** | 多父继承、换脑、跨境闸门 | [model_gateway.md](model_gateway.md) | [schema](schemas/model_gateway.schema.json) |
| 5 | **LifePack** 生命包 | 迁移 / 恢复 / 继承；基因组永不进主包 | [lifepack.md](lifepack.md) | [schema](schemas/lifepack.schema.json) |
| 6 | 一体多身**同步整合** | 多设备并集 + 向量时钟；语义冲突三层整合 | [sync_merge.md](sync_merge.md) | [schema](schemas/sync_merge.schema.json) |

公共枚举与基础类型见 [common_defs](schemas/common_defs.schema.json)：CoreId（self/companion/mentor）、路由 L0-L3、风险 A0-A4、信任 T0-T5、真值状态、向量时钟等。

## 三条不可协商的原则（任何实现都必须守）

一个实现只有守住这三条，才配叫"三生"：

1. **数据归主人，隐私永不入种群。** 只有脱敏的方法/能力基因可在种群间传播；任何私人数据的传播在协议层就被拒绝（`memory_record` 的 `consent.population_share` 恒为 `false`）。
2. **不冒充。** 事实、推断、想象在 `truth_state` 上永不混淆；不冒充真人、不伪造记忆。
3. **可被终止。** 天性/宪章层不可被"进化"解除；资金的最后一击永远归人；一切外部动作可暂停、可回滚、可审计。

## 怎么算"三生兼容"（Conformance）

一个实现声称兼容三生开放协议，至少要满足：

- 它的数据能通过本目录 `schemas/` 的校验；
- 它守住上面三条原则；
- 它满足这些**关键不变式**（也是我们自己的验收）：
  - "现在几点"走 L0，**三核模型零调用**；
  - 任一核**不得越权读另一核私域**；
  - 高风险不可逆动作（A3/A4）进 **Safe Pause** 或需**授权**，不因句子里含"现在"被 L0 抢匹配；
  - 记忆 `population_share` 恒 `false`，基因组不进 LifePack 主包；
  - L3 保留三视角与少数意见，**不产生多数票**。

## 自己校验（可运行）

```bash
# 需要 python + jsonschema + referencing
pip install jsonschema referencing
python schemas/validate_contracts.py
```

会对每份 Schema 跑一组合法/非法样例。**21/21 通过 = 数据合规**，且 8 个故意写错的样例（隐私想进种群、天性想被改、基因组进主包、L0 调模型、L3 缺三视角……）全部被如期拒绝——这就是"标准能挡住错误"的意思。

## 版本与治理（怎么改这个标准）

- 当前 **v0.1 草案**，冻结前会变；方向是稳的。
- **提意见**：开 [Issue](../../issues)（`spec` 标签）或来 [Discussions](../../discussions)。
- **改动走 ADR**：用 supersedes 追加、不静默改写历史。
- 冻结后按语义化版本演进；破坏性变更给迁移工具与迁移说明。

## 许可

本协议（说明文档与 JSON Schema）以 **Apache-2.0** 开放，自由实现、自由分发。**开放的是协议，不是任何人的人生**——代码与格式开源，用户的记忆、隐私、基因永远归用户。
