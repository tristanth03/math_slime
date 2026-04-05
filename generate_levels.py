#!/usr/bin/env python3
"""Pre-generate all MathSlime question pools -> docs/levels.json"""
import json, os

def plus_pool(lo, hi):
    return [{"t": f"{a} + {b}", "a": a + b}
            for a in range(lo, hi + 1) for b in range(lo, hi + 1)]

def minus_pool(lo, hi, nonneg_only=False):
    pool = []
    for a in range(lo, hi + 1):
        for b in range(lo, hi + 1):
            r = a - b
            if nonneg_only and r < 0:
                continue
            pool.append({"t": f"{a} - {b}", "a": r})
    return pool

pools = [
    plus_pool(1, 5),           # 0: +  {1..5}
    plus_pool(0, 10),          # 1: +  {0..10}
    minus_pool(0, 5, True),    # 2: -  {0..5} non-neg only
    minus_pool(0, 5, False),   # 3: -  {0..5} full (negatives)
    plus_pool(0, 20),          # 4: +  {0..20}
]

levels = [
    None,
    # 1-2: Baby Steps — plus {1..5}
    {"name":"Baby Steps",       "d":5,"n":3, "boss":None,  "ch":3,"p":[0]},
    {"name":"Baby Steps",       "d":5,"n":5, "boss":"mini","ch":3,"p":[0]},
    # 3-5: One More Step — plus {0..10}
    {"name":"One More Step",    "d":5,"n":6, "boss":None,  "ch":4,"p":[1]},
    {"name":"One More Step",    "d":5,"n":7, "boss":None,  "ch":4,"p":[1]},
    {"name":"One More Step",    "d":5,"n":8, "boss":"mega","ch":4,"p":[1]},
    # 6-8: Minus? — plus {0..10} + minus non-neg {0..5}
    {"name":"Minus?",           "d":5,"n":6, "boss":None,  "ch":4,"p":[1,2]},
    {"name":"Minus?",           "d":5,"n":7, "boss":None,  "ch":4,"p":[1,2]},
    {"name":"Minus?",           "d":5,"n":8, "boss":"mini","ch":4,"p":[1,2]},
    # 9-12: Negative Numbers — plus {0..10} + minus full {0..5}
    {"name":"Negative Numbers", "d":5,"n":6, "boss":None,  "ch":4,"p":[1,3]},
    {"name":"Negative Numbers", "d":5,"n":7, "boss":None,  "ch":4,"p":[1,3]},
    {"name":"Negative Numbers", "d":5,"n":8, "boss":None,  "ch":4,"p":[1,3]},
    {"name":"Negative Numbers", "d":5,"n":10,"boss":"mega","ch":4,"p":[1,3]},
    # 13-15: Twenty What? — plus {0..20} + minus full {0..5}
    {"name":"Twenty What?",     "d":5,"n":6, "boss":None,  "ch":5,"p":[4,3]},
    {"name":"Twenty What?",     "d":5,"n":7, "boss":None,  "ch":5,"p":[4,3]},
    {"name":"Twenty What?",     "d":5,"n":8, "boss":"mini","ch":5,"p":[4,3]},
    # 16: Mixed Review
    {"name":"Mixed Review",     "d":5,"n":8, "boss":None,  "ch":5,"p":[4,3]},
    # 17-18: Speed
    {"name":"Ready for Speed?", "d":6,"n":4, "boss":None,  "ch":5,"p":[4,3]},
    {"name":"Speed Demon",      "d":7,"n":10,"boss":"mega","ch":5,"p":[4,3]},
]

data = {"pools": pools, "levels": levels}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "levels.json")
with open(out, "w") as f:
    json.dump(data, f, separators=(",", ":"))

print(f"Wrote {out} ({os.path.getsize(out)} bytes)")
for i, lv in enumerate(levels):
    if lv:
        total = sum(len(pools[j]) for j in lv["p"])
        print(f"  Lv{i:2d}: {lv['name']:20s} | d={lv['d']} | {lv['n']:2d} problems | {total:4d} in pool | boss={lv['boss']}")
