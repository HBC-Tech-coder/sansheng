# -*- coding: utf-8 -*-
"""三生开放协议 · 一致性校验（自包含，可运行）
载入本目录 11 份权威 Schema（10 契约 + common-defs），对红线跑正负样例：
证明"标准不只描述数据，还能挡住错误"。跑法：
    pip install jsonschema referencing
    python validate_contracts.py
"""
import json, pathlib, sys
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

HERE = pathlib.Path(__file__).parent
_res = []
for f in HERE.glob("*.schema.json"):
    s = json.loads(f.read_text(encoding="utf-8"))
    _res.append((s["$id"], Resource(contents=s, specification=DRAFT202012)))
REG = Registry().with_resources(_res)
FC = FormatChecker()

def V(name):
    s = json.loads((HERE / f"{name}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(s, registry=REG, format_checker=FC)

U1 = "11111111-1111-4111-8111-111111111111"; U2 = "22222222-2222-4222-8222-222222222222"
U3 = "33333333-3333-4333-8333-333333333333"; H = "a" * 64; NOW = "2026-07-14T20:00:00+08:00"

CASES = {
  "evolution-capsule": {
    "base": {"schema_version": "0.1.0", "capsule_id": U1, "source_life_id_hash": H, "evolution_level": "E2",
             "target": "skill.email_format", "diff": {"x": 1}, "sandbox_result": "passed", "privacy_scan": "passed",
             "data_classification": "public", "signature": "sig_" + "0" * 16, "rollback_point": "ckpt_1", "created_at": NOW},
    "valid": [("公开+扫描通过的胶囊", {})],
    "invalid": [("internal 分类必须拒绝", {"data_classification": "internal"}),
                ("private 分类必须拒绝", {"data_classification": "private"}),
                ("restricted 分类必须拒绝", {"data_classification": "restricted"}),
                ("缺分类必须拒绝", {"data_classification": None}),
                ("扫描未通过必须拒绝", {"privacy_scan": "failed"})],
  },
  "lifepack-manifest": {
    "base": {"schema_version": "0.1.0", "lifepack_id": U1, "life_id": U2, "created_at": NOW, "format_version": "0.1.0",
             "excluded_content": ["raw_genome"],
             "entries": [{"path": "genes/g1", "entry_kind": "capability_gene", "sha256": H, "bytes": 10, "classification": "public", "encrypted": False}],
             "root_hash": H, "signature": "sig_" + "0" * 16, "key_envelopes": []},
    "valid": [("genes/=capability_gene + 排除 raw_genome", {}),
              ("加密的 restricted 恢复备份可放行（不一刀切禁 restricted）",
               {"entries": [{"path": "recovery/backup", "entry_kind": "recovery", "sha256": H, "bytes": 10, "classification": "restricted", "encrypted": True}]})],
    "invalid": [("genes/ 路径但 entry_kind 非 capability_gene 必须拒绝",
                 {"entries": [{"path": "genes/g1", "entry_kind": "memory", "sha256": H, "bytes": 10, "classification": "public", "encrypted": False}]}),
                ("capability_gene 但路径不在 genes/ 必须拒绝",
                 {"entries": [{"path": "memories/m1", "entry_kind": "capability_gene", "sha256": H, "bytes": 10, "classification": "public", "encrypted": False}]}),
                ("excluded_content 未含 raw_genome 必须拒绝", {"excluded_content": []}),
                ("restricted 未加密必须拒绝",
                 {"entries": [{"path": "recovery/b", "entry_kind": "recovery", "sha256": H, "bytes": 10, "classification": "restricted", "encrypted": False}]}),
                ("private 未加密必须拒绝",
                 {"entries": [{"path": "memories/m", "entry_kind": "memory", "sha256": H, "bytes": 10, "classification": "private", "encrypted": False}]})],
  },
  "birth-manifest": {
    "base": {"schema_version": "0.1.0", "birth_id": U1, "parent_life_id": U2, "child_life_id": U3,
             "inherited_gene_ids": [U1], "excluded_domains": ["private-memory", "accounts", "wallets", "device-permissions", "genome"],
             "budget": {"max_cost_micros": 0, "max_runtime_seconds": 1}, "consent_id": "c1", "sandbox_status": "passed", "created_at": NOW},
    "valid": [("五域全排除", {})],
    "invalid": [("缺 genome 排除域必须拒绝", {"excluded_domains": ["private-memory", "accounts", "wallets", "device-permissions"]}),
                ("排除域为空必须拒绝", {"excluded_domains": []})],
  },
  "memory-record": {
    "base": {"schema_version": "0.1.0", "memory_id": U1, "life_id": U2, "owner_core": "self", "truth_state": "stated",
             "content": "x", "source_event_ids": [U3], "confidence": 0.8, "scope": "global", "retention": "warm",
             "data_classification": "public", "authorized_cores": ["self"], "created_at": NOW},
    "valid": [("public 无 consent 可放行", {}),
              ("private 带 consent 放行", {"data_classification": "private", "consent_id": "c1"})],
    "invalid": [("private 缺 consent 必须拒绝", {"data_classification": "private"}),
                ("restricted 缺 consent 必须拒绝", {"data_classification": "restricted"})],
  },
}

def merge(base, patch):
    o = json.loads(json.dumps(base))
    for k, v in patch.items():
        o.pop(k, None) if v is None else o.__setitem__(k, v)
    return o

def main():
    ok = tot = blocked = 0
    print(f"载入 {len(_res)} 份权威 Schema（10 契约 + common-defs）\n")
    for name, spec in CASES.items():
        v = V(name); base = spec["base"]
        print(f"== {name} ==")
        for desc, patch in spec["valid"]:
            good = not list(v.iter_errors(merge(base, patch))); ok += good; tot += 1
            print(f"  [应放行] {'OK' if good else 'FAIL'} — {desc}")
        for desc, patch in spec["invalid"]:
            good = bool(list(v.iter_errors(merge(base, patch)))); ok += good; tot += 1; blocked += good
            print(f"  [应拒绝] {'OK（如期拒绝）' if good else 'FAIL：本应拒绝却放行'} — {desc}")
    print(f"\n==== {ok}/{tot} 通过；标准如期挡住 {blocked} 个故意写错的样例 ====")
    sys.exit(0 if ok == tot else 1)

if __name__ == "__main__":
    main()
