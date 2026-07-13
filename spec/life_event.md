> **草案 DRAFT v0.1** — 这是三生「AI 生命体互操作开放标准」的早期草案，冻结前可能变化。
> Early draft of the SanSheng open interoperability standard for digital life; may change before freeze.

# SPEC · 生命事件 LifeEvent（契约草案 v0.1）

> 状态：草案，待 Claude / codex 双签。依据 v2 文档 §4.1、§16.4。
> 生命的最小存在单位。三核共享同一条事件总线，一切记忆/账单/审计由事件派生。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | string(uuid) | 事件唯一 ID |
| event_time | ISO8601 | 现实中事件发生的时间 |
| record_time | ISO8601 | 系统知道/记录该事件的时间（双时间） |
| source | enum | voice / text / file / sensor / model / skill / device / payment / system |
| actor | enum | mirror / companion / sage / master / external |
| permission | enum | 触发所需/所用的权限等级（对应信任账户 L0-L5） |
| risk | enum | A0 / A1 / A2 / A3 / A4（行动网关分级，决定快/慢通路） |
| content | object | 事件内容（结构随 source 而定） |
| evidence | string(hash)? | 原始证据哈希（可溯源） |
| cost | object? | { tokens, money, model } 成本 |
| result | object? | 执行结果 / 用户修改 / 失败原因 |
| signature | string? | 高风险事件的签名 |

## 约束

- 只追加，不可篡改（append-only）。支持幂等、重试、顺序、审计。
- 涉及资金 / 对外发布 / 设备动作的事件必须带确认状态与撤销/补偿方案。
- 存储：正本用 JSONL / SQLite；索引可重建。

## 待双方确认的分歧点

- [ ] content 的 schema 是强类型（每种 source 一个 schema）还是弱类型（自由 JSON）？
- [ ] 成本 cost 记在事件上还是单独账本表？
- [ ] 事件与记忆的关系：事件 → 派生记忆，用什么字段关联？
