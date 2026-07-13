> **草案 DRAFT v0.1** — 这是三生「AI 生命体互操作开放标准」的早期草案，冻结前可能变化。
> Early draft of the SanSheng open interoperability standard for digital life; may change before freeze.

# SPEC · 多模型混血网关（契约草案 v0.1）

> 状态：草案，待双签。依据 v2 文档 §3.6、§10.4。
> 目标：突破 Hermes"只接一个模型"的限制。三生是多个大模型共同的"孩子"。

## 接口

```
ModelGateway.call(req) -> resp
  req = {
     task_type,            // chat / reason / code / vision / ...
     messages,
     model: ModelRef | "auto",  // 指定生父，或由路由器选
     stream: bool,
     budget: {max_tokens, max_cost}
  }
```

## 多父继承（混血）

- 统一适配 Claude / OpenAI / 图灵九歌(本土兜底) / 开源本地模型；标准化输入输出、流式、计费、错误、超时、重试、降级。
- 三核可各绑不同生父（镜核=最懂中文细腻表达的模型；贤核代码席位=最强代码模型；伴核=高性价比模型）。
- **慢通路多模型融合**：同一视角可由多个模型并行给出、再融合（取两家之长，不是二选一）。

## 血统档案（动态）

```
ModelProfile = { name, vendor, strengths[], cost_per_1k, latency_ms,
                 success_rate: {[task_type]: float}, stability }
```
路由器据此为每个任务组织"这次由哪几位生父参与"。模型换代后重新评测，防漂移。

## 换脑手术

- 新模型先在隔离环境读同一 LifePack，过身份/价值/记忆/关系/安全回归测试。
- 新旧并行比对漂移 → 达标切换 → 保留回滚检查点。
- **换脑回归测试集**是最重要的自研资产（放 TESTS/）。

## 待双方确认

- [ ] ModelRef 的统一标识格式？
- [ ] "融合多模型视角"的具体策略（投票？加权？裁判模型？）？
- [ ] 本地模型（Ollama 等）的接入优先级？
