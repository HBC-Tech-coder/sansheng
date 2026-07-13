> **草案 DRAFT v0.1** — 这是三生「AI 生命体互操作开放标准」的早期草案，冻结前可能变化。
> Early draft of the SanSheng open interoperability standard for digital life; may change before freeze.

# SPEC · 记忆记录 MemoryRecord（契约草案 v0.1）

> 状态：草案，待双签。依据 v2 文档 §4.3、§16.4。
> 四层记忆：事件层(正本)→知识层(结构,人类可读)→自我层(叙事)→索引层(缓存,可重建)。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | string | 记忆 ID |
| truth_state | enum | observed(已观察) / stated(本人陈述) / reported(外部报告) / inferred(模型推断) / imagined(想象梦境) / disputed(有争议) / retracted(已撤回) |
| content | string/md | 记忆内容（人类可读 Markdown 优先） |
| source_id | string | 关联的 LifeEvent / 文件 / 对话 |
| evidence_hash | string? | 原始证据哈希 |
| confidence | float | 置信度 0-1 |
| scope | string | 适用范围（全局/某项目/某关系…） |
| retention | enum | 冷/热/温；遗忘策略 |
| consent | object | 同意范围（谁可读；能否入种群=永远否） |
| authorized_cores | [enum] | 哪些核可读（镜/伴/贤，最小权限） |
| supersedes | string? | 纠错链：此记录取代了哪条（不抹历史） |
| model_version | string | 写入时的底层模型（换脑追溯用） |
| signature | string? | 签名 |

## 约束

- **事实 / 推断 / 想象 永不混淆**（truth_state 强制）。
- 纠错不删除历史，建 supersedes 链（过去如何理解→为何更正→现在什么有效）。
- 人类可读是百年可迁移的前提：知识层用 Markdown + 图谱，向量只是可重建缓存。
- 隐私记忆永远不进种群、不进接单工作副本（只带脱敏副本）。

## 待双方确认

- [ ] 三核共享的"对主人的建模"用 Honcho 式共享 workspace 还是自建？
- [ ] 冷热分层的自动升降规则？
- [ ] 遗忘=降权归档（可逆）vs 焚毁（不可逆）的触发与审批？
