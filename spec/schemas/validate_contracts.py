# -*- coding: utf-8 -*-
"""三生契约校验器：证明六份契约是"可校验"的。
用法: python validate_contracts.py
对每个 schema 跑一组 VALID（应通过）和 INVALID（应各自因预期原因失败）样例。
全绿 = 契约可机器校验，可作为双签冻结的依据。"""
import json, sys, pathlib
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = pathlib.Path(__file__).parent

def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

# 用 registry 解析 common_defs 的跨文件 $ref
files = ["common_defs.schema.json", "life_event.schema.json", "memory_record.schema.json",
         "decision_trace.schema.json", "model_gateway.schema.json", "sync_merge.schema.json",
         "lifepack.schema.json"]
resources = []
for f in files:
    s = load(f)
    resources.append((s["$id"].split("/")[-1], Resource.from_contents(s)))
registry = Registry().with_resources(resources)

def V(schema_file):
    return Draft202012Validator(load(schema_file), registry=registry)

NOW = "2026-07-13T20:00:00+08:00"
DEV = "dev_home01"
VC  = {DEV: 3}

CASES = {
  "life_event.schema.json": {
    "valid": [
      {"id":"evt_abc123","life_id":"life_sunbo","event_time":NOW,"record_time":NOW,
       "source":"text","actor":"master","risk":"A0","content":{"text":"现在几点"},
       "content_hash":"sha256:"+"0"*64,"device_id":DEV,"vector_clock":VC},
      {"id":"evt_pay01","life_id":"life_sunbo","event_time":NOW,"record_time":NOW,
       "source":"payment","actor":"companion","risk":"A3","content":{"amount":225},
       "content_hash":"sha256:"+"1"*64,"device_id":DEV,"vector_clock":VC,
       "confirmation":{"status":"pending","compensation":"退款"}},
    ],
    "invalid": [
      ("A3 事件缺 confirmation 必须失败",
       {"id":"evt_x","life_id":"life_sunbo","event_time":NOW,"record_time":NOW,"source":"payment",
        "actor":"companion","risk":"A3","content":{},"content_hash":"sha256:"+"2"*64,
        "device_id":DEV,"vector_clock":VC}),
      ("非法 risk 值必须失败",
       {"id":"evt_y","life_id":"life_sunbo","event_time":NOW,"record_time":NOW,"source":"text",
        "actor":"master","risk":"A9","content":{},"content_hash":"sha256:"+"3"*64,
        "device_id":DEV,"vector_clock":VC}),
      ("缺 vector_clock（同步必需）必须失败",
       {"id":"evt_z","life_id":"life_sunbo","event_time":NOW,"record_time":NOW,"source":"text",
        "actor":"master","risk":"A0","content":{},"content_hash":"sha256:"+"4"*64,"device_id":DEV}),
    ],
  },
  "memory_record.schema.json": {
    "valid": [
      {"id":"mem_001","life_id":"life_sunbo","truth_state":"inferred",
       "content":"主人近期更看重现金流安全","source_ids":["evt_abc123"],"confidence":0.72,
       "scope":"global","retention":"warm","consent":{"population_share":False},
       "authorized_cores":["self","companion"],"created_at":NOW},
    ],
    "invalid": [
      ("population_share=true 必须失败（隐私永不入种群）",
       {"id":"mem_x","life_id":"life_sunbo","truth_state":"observed","content":"x",
        "source_ids":["evt_1"],"confidence":1,"scope":"global","retention":"hot",
        "consent":{"population_share":True},"authorized_cores":["self"],"created_at":NOW}),
      ("缺 source_ids（记忆必须可溯源）必须失败",
       {"id":"mem_y","life_id":"life_sunbo","truth_state":"observed","content":"x","confidence":1,
        "scope":"global","retention":"hot","consent":{"population_share":False},
        "authorized_cores":["self"],"created_at":NOW}),
      ("非法 truth_state 必须失败",
       {"id":"mem_z","life_id":"life_sunbo","truth_state":"fact","content":"x","source_ids":["e"],
        "confidence":1,"scope":"global","retention":"hot","consent":{"population_share":False},
        "authorized_cores":["self"],"created_at":NOW}),
    ],
  },
  "decision_trace.schema.json": {
    "valid": [
      {"trace_id":"trace_l0","life_id":"life_sunbo","action":"route","route_level":"L0",
       "lead_core":"life-kernel","risk":"A0","created_at":NOW,"model_receipts":[]},
      {"trace_id":"trace_l3","life_id":"life_sunbo","action":"route","route_level":"L3","risk":"A3",
       "created_at":NOW,"decider":"master","positions":[
         {"core":"self","view":"你要的是稳中求进","confidence":0.84},
         {"core":"companion","view":"现金流能撑200万验证","confidence":0.7},
         {"core":"mentor","view":"三种最可能失败方式","confidence":0.6}]},
      {"trace_id":"trace_sp","life_id":"life_sunbo","action":"safe_pause","route_level":None,
       "risk":"A4","created_at":NOW},
    ],
    "invalid": [
      ("L0 带 model_receipts 必须失败（现在几点不调模型）",
       {"trace_id":"trace_bad","life_id":"life_sunbo","action":"route","route_level":"L0","risk":"A0",
        "created_at":NOW,"model_receipts":[{"model":{"provider":"x","model":"y"},"role":"lead"}]}),
      ("L3 缺 positions 必须失败（必须保留三视角）",
       {"trace_id":"trace_bad2","life_id":"life_sunbo","action":"route","route_level":"L3","risk":"A3",
        "created_at":NOW,"decider":"master"}),
    ],
  },
  "sync_merge.schema.json": {
    "valid": [
      {"merge_receipts":[
        {"id":"merge_1","life_id":"life_sunbo","object_kind":"fact",
         "resolution":"supersede_newer_keep_branch","resolver":"auto","kept_branches":2,"created_at":NOW},
        {"id":"merge_2","life_id":"life_sunbo","object_kind":"value",
         "resolution":"escalated_to_master","resolver":"master","kept_branches":2,"created_at":NOW},
        {"id":"merge_3","life_id":"life_sunbo","object_kind":"nature_constitution",
         "resolution":"tamper_alarm","resolver":"immune_system","kept_branches":1,"created_at":NOW}]},
    ],
    "invalid": [
      ("价值层自动合并必须失败（必须上抛主人）",
       {"merge_receipts":[{"id":"merge_x","life_id":"life_sunbo","object_kind":"value",
         "resolution":"auto_union","resolver":"auto","kept_branches":2,"created_at":NOW}]}),
      ("天性层被当普通合并必须失败（应为篡改告警）",
       {"merge_receipts":[{"id":"merge_y","life_id":"life_sunbo","object_kind":"nature_constitution",
         "resolution":"auto_union","resolver":"auto","kept_branches":1,"created_at":NOW}]}),
    ],
  },
  "lifepack.schema.json": {
    "valid": [
      {"schema_version":"0.1","life_id":"life_sunbo","created_at":NOW,
       "sections":{"identity":{"hash":"sha256:"+"a"*64,"encrypted":True}},
       "excludes":["raw_genome"],"signature":"sig..."},
    ],
    "invalid": [
      ("excludes 不含 raw_genome 必须失败（基因组永不进主包）",
       {"schema_version":"0.1","life_id":"life_sunbo","created_at":NOW,
        "sections":{"identity":{"hash":"sha256:"+"a"*64,"encrypted":True}},
        "excludes":["nothing"],"signature":"sig"}),
    ],
  },
  "model_gateway.schema.json": {
    "valid": [
      {"request":{"task_type":"chat","messages":[],"model":"auto","account_mode":"byo_key"}},
    ],
    "invalid": [
      ("非法 account_mode 必须失败",
       {"request":{"task_type":"chat","messages":[],"model":"auto","account_mode":"free"}}),
    ],
  },
}

def main():
    total=passed=0
    for schema_file, cases in CASES.items():
        v = V(schema_file)
        print(f"\n== {schema_file} ==")
        for obj in cases.get("valid", []):
            total+=1; errs=list(v.iter_errors(obj))
            ok = not errs
            passed+=ok
            print(f"  [VALID ] {'OK' if ok else 'FAIL: '+errs[0].message}")
        for reason, obj in cases.get("invalid", []):
            total+=1; errs=list(v.iter_errors(obj))
            ok = bool(errs)  # 预期失败
            passed+=ok
            print(f"  [INVALID] {'OK（如期拒绝）' if ok else 'FAIL：本应被拒却通过了'} — {reason}")
    print(f"\n==== {passed}/{total} 通过 ====")
    sys.exit(0 if passed==total else 1)

if __name__=="__main__":
    main()
