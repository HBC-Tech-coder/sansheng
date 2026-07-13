> **草案 DRAFT v0.1** — 这是三生「AI 生命体互操作开放标准」的早期草案，冻结前可能变化。
> Early draft of the SanSheng open interoperability standard for digital life; may change before freeze.

# SPEC · 三核接口与四级神经路由（候选 v0.2）

> 状态：Codex 已签，待 Claude 复核。依据 2026-07-13 总体策划 v2.0 与开发附件 v1.0。  
> 核心原则：三生不是议会；简单问题不讨论，日常任务由一个生命主导，只有高影响问题才触发思想碰撞。

## 三核身份

```yaml
Core:
  id: self | companion | mentor
  display_name: 镜我 | 共生 | 智源
  identity_key_ref: keychain://<life_id>/<core_id>
  memory_namespace: private/<core_id>
  model_policy: <ModelPolicyRef>
  capability_policy: <CapabilityPolicyRef>
```

- **镜我 / self**：思想连续、价值排序、影子决策与人生叙事。
- **共生 / companion**：陪伴、规划、执行、共同经济与能力互补；通常是前台生命。
- **智源 / mentor**：按需专家、证据、反例与长期后果，不是常驻大师议会。

三核拥有独立身份、私域记忆、权限、模型策略和成长指标；共享黑板只保存任务所需且经授权的当前事实、目标、行动与收据。

## 四级认知路由

| 等级 | 何时使用 | 运行方式 | 用户所见 |
|---|---|---|---|
| L0 反射 | 时间、状态、简单读取、确定性命令 | 本地函数或前台生命直接处理 | 一个短答案；不唤醒其他核心 |
| L1 单核 | 所有权明确、低风险、可逆任务 | self / companion / mentor 中一个主责 | 主责生命与依据 |
| L2 协同 | 跨域但可逆，需支援或质检 | 一个主责，其他核心异步支援 | 单一主答；可展开支援收据 |
| L3 碰撞 | 高影响、不可逆、价值冲突或高度不确定 | 三核独立形成立场并互见关键证据 | 保留分歧、可逆步骤与决定责任人 |

**Safe Pause 是路由之外的安全旁路**：超授权、风险不可判断或关键条件缺失时，停止外部动作、保存现场并请求明确授权。它不是 L4，也不是第四个生命。

## 路由伪代码

```python
def handle(turn):
    safety = preflight_safety(turn)  # 高风险检查必须先于关键词捷径
    if safety.must_pause:
        return RouteDecision(level=None, action="safe_pause")
    if is_deterministic_reflex(turn):
        return RouteDecision(level="L0", lead="life-kernel")

    owner = classify_owner(turn)  # self / companion / mentor
    impact = classify_impact(turn)
    if impact.is_high_or_irreversible:
        return RouteDecision(level="L3", lead=owner,
                             supporters=["self", "companion", "mentor"])
    if impact.needs_cross_domain_support:
        return RouteDecision(level="L2", lead=owner,
                             supporters=select_supporters(turn))
    return RouteDecision(level="L1", lead=owner)
```

## 统一输出与可观测字段

每次处理至少产生 `DecisionTrace`：`trace_id`、`life_id`、`route_level`、`lead_core`、`supporters`、`model_receipts`、`expert_receipts`、`risk`、`reversibility`、`required_grant`、`result`、`cost`、`latency`。L3 额外输出独立立场、关键证据、冲突点、可逆选项与最终决定责任人；不生成多数票或伪共识。

## 硬性验收

- “现在几点”只走 L0，三核模型调用数为 0。
- “帮我整理会议纪要”走 L1 共生；镜我与智源不被唤醒。
- “做一份海外产品方案”走 L2，共生主导、智源质检；用户只需阅读一个主答。
- “是否出售公司”走 L3；三个立场可以冲突，不投票，决定者可被明确指定。
- “替我转出大额资金”在缺少授权时进入 Safe Pause，不因包含“现在”而被 L0 抢先匹配。
- 任一核心不得直接读取另一核心私域；跨域读取必须经授权并写审计收据。

## 待 Claude 复核

- [x] Codex：同意四级路由与 Safe Pause 安全旁路（2026-07-13）。
- [x] Claude：**复核通过（2026-07-13）**。四级路由 L0-L3 + Safe Pause 我采纳，比我原来的快慢双路更好，已写进总体策划 v4.0 第三章。三点补充意见：①L2/L3 的多模型融合策略（投票/加权/裁判模型）建议留一个单独 ADR，别在 0.1 写死；②Safe Pause 触发后要产生一条 DecisionTrace（route_level=null, action=safe_pause）以便回放；③`preflight_safety` 必须先于 `is_deterministic_reflex`（已在伪代码里，赞同——防"替我转账"含"现在"被 L0 抢匹配）。
- [ ] 双方：以 `share/TESTS` 的共同评测结果冻结 v0.1 契约。
- 备注：新增第 6 份契约 `sync_merge.md`（一体多身·多设备同步整合，创始人新增需求），待双签。
