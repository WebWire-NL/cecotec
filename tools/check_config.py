#!/usr/bin/env python3
"""Check a tuya-local device config against a real device status dump.

Answers the three questions that matter when adapting a config to your own robot:

  * does the config declare datapoints your device does not report?
  * does your device report datapoints the config does not cover?
  * does a declared type disagree with what the device actually sends?

Usage
-----
    python3 tools/check_config.py --config CONFIG.yaml --dump dump.json

    # or fetch live (needs tinytuya installed)
    python3 tools/check_config.py --config CONFIG.yaml --live \
        --host 192.168.1.50 --device-id ID --local-key KEY

`dump.json` may be either the whole status reply ({"dps": {...}}) or just the
datapoint map ({"1": false, ...}).

Exit code is 1 if a type mismatch is found, so it can run in CI. Missing and
extra datapoints are reported but do not fail: write-only function datapoints
legitimately never appear in a dump.
"""
import argparse
import json
import sys

try:
    import yaml
except ImportError:
    sys.exit("needs PyYAML: pip install pyyaml")

# How a declared datapoint type compares to what arrives on the wire.
# Declared -> family. Families: bool, num, str, raw (raw accepts anything).
FAMILY = {
    "boolean": "bool",
    "integer": "num",
    "bitfield": "num",
    "string": "str",
    "base64": "str",  # a base64 blob arrives as a string; an int here is a real bug
    "json": "raw",
    "raw": "raw",
}


def live_family(value):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "num"
    if isinstance(value, str):
        return "str"
    return "other"


def load_config(path):
    with open(path) as fh:
        doc = yaml.safe_load(fh)
    rows = []
    for ent in doc.get("entities") or []:
        kind = ent.get("entity", "?")
        label = ent.get("name") or ent.get("translation_key") or kind
        for dp in ent.get("dps") or []:
            rows.append(
                {
                    "id": str(dp.get("id")),
                    "type": dp.get("type", "?"),
                    "optional": bool(dp.get("optional")),
                    "where": f"{kind} / {label}",
                    "raw": dp,
                }
            )
    products = [p.get("id") for p in doc.get("products") or []]
    return doc, rows, products


def load_dump(args):
    if args.live:
        try:
            import tinytuya
        except ImportError:
            sys.exit("--live needs tinytuya: pip install tinytuya")
        dev = tinytuya.Device(args.device_id, args.host, args.local_key, version=3.3)
        dev.set_socketTimeout(6)
        reply = dev.status()
        if "dps" not in reply:
            sys.exit(f"device did not return dps: {reply}")
        return reply["dps"]
    with open(args.dump) as fh:
        data = json.load(fh)
    return data.get("dps", data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--dump")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--host")
    ap.add_argument("--device-id")
    ap.add_argument("--local-key")
    args = ap.parse_args()
    if not args.live and not args.dump:
        ap.error("give --dump FILE or --live")

    doc, rows, products = load_config(args.config)
    dps = {str(k): v for k, v in load_dump(args).items()}

    print(f"config : {args.config}")
    print(f"product: {', '.join(str(p) for p in products) or '(none declared)'}")
    print(f"        {len(rows)} declared datapoints across {len(doc.get('entities') or [])} entities")
    print(f"dump   : {len(dps)} datapoints reported by the device")
    print()

    mismatches, missing = [], []
    for row in rows:
        if row["id"] not in dps:
            missing.append(row)
            continue
        want = FAMILY.get(row["type"], "raw")
        got = live_family(dps[row["id"]])
        if want != "raw" and got != "other" and want != got:
            mismatches.append((row, got, dps[row["id"]]))

    covered = {row["id"] for row in rows}
    extra = sorted((int(k) for k in dps if k not in covered))

    if mismatches:
        print("TYPE MISMATCHES (config vs live) — these will misbehave")
        for row, got, value in mismatches:
            print(f"  DP {row['id']:<4} config={row['type']:<8} live={got:<4} "
                  f"value={value!r:<28} in {row['where']}")
        print()

    mapped = [row for row in missing if not row["optional"]]
    optional = [row for row in missing if row["optional"]]
    if mapped:
        print("DECLARED REQUIRED BUT NOT IN DUMP — wrong id, or write-only")
        for row in mapped:
            print(f"  DP {row['id']:<4} {row['type']:<8} in {row['where']}")
        print()
    if optional:
        print(f"declared optional, not in dump ({len(optional)}) — fine if write-only")
        print("  " + ", ".join(row["id"] for row in optional))
        print()

    if extra:
        print("IN DUMP, NOT IN CONFIG — unmapped datapoints")
        for dp_id in extra:
            value = dps[str(dp_id)]
            print(f"  DP {dp_id:<4} {live_family(value):<5} = {value!r}")
        print()

    if not mismatches and not mapped and not extra:
        print("clean: the config and the device agree in both directions")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
