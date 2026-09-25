# Cecotec Conga 11090 Spin Revolution Home&Wash — Home Assistant (local)

Local (cloud-free) Home Assistant support for the **Cecotec Conga 11090 Spin Revolution
Home&Wash** robot vacuum, plus the reusable pieces around it: a template for the whole
Tuya "standard sweeper" family of robots, a map of which datapoint generation each brand
uses, and a checker that tells you whether a config matches your own machine.

The robot is a Tuya device behind Cecotec's branded app, so once you have its local key it
talks plain Tuya LAN protocol on port 6668.

Product ID: `kazdsquasfw0gmrn` · category `sd` · Tuya protocol **3.3**

## What's in here

| Path | What it is |
|---|---|
| `devices/cecotec_conga_11090_vacuum.yaml` | Device config for [tuya-local](https://github.com/make-all/tuya-local) — 25 entities |
| `templates/tuya_sweeper_standard_a.yaml` | Template for any robot on the same standard sweeper layout, other brands included |
| `docs/dp-map.md` | This model's datapoint map, including what is known about its vendor-specific datapoints |
| `docs/sweeper-dp-generations.md` | Which datapoint generation each Tuya vacuum brand and model uses |
| `tools/check_config.py` | Compare a config against a real device dump: type mismatches, coverage, unmapped datapoints |

Every datapoint and value range in the device config was confirmed against what the vacuum
itself reports over the LAN.

## If your robot is not this model

The Tuya standard sweeper layout is shared across rebadges — ILIFE, ABIR, Neatsvor,
Proscenic, Medion, Liectroux, Rowenta, Kogan, Kabum, Blaupunkt, Ttec, Gadnic and Cecotec
among them. Those brands ship the same datapoint semantics with different product IDs, so a
config written for one is usually the right starting point for another.

1. Dump your robot and read the datapoint numbers it reports:

   ```python
   import tinytuya, json
   d = tinytuya.Device("<device_id>", "<ip>", "<local_key>", version=3.3)
   d.set_socketTimeout(6)
   print(json.dumps(d.status().get("dps", {}), indent=1, sort_keys=True))
   ```

2. Match that against `docs/sweeper-dp-generations.md` to find your device's generation.
3. Copy the matching template or config, swap in your own product ID, and delete what your
   device does not report.
4. Check the result against the dump:

   ```
   python3 tools/check_config.py --config your_config.yaml --dump dump.json
   ```

   It reports datapoints your device sends that the config ignores, datapoints the config
   declares that never arrive, and any declared type that disagrees with what the device
   actually sends. It exits non-zero on a type mismatch, so it works as a CI gate.

## Requirements

- Home Assistant with [HACS](https://hacs.xyz/)
- [tuya-local](https://github.com/make-all/tuya-local) installed as a HACS **custom repository**
- Your vacuum on the same network as Home Assistant

## Install

1. In HACS → Integrations → ⋮ → *Custom repositories* → add
   `https://github.com/make-all/tuya-local` as type **Integration**, then install it.
2. Copy `devices/cecotec_conga_11090_vacuum.yaml` into
   `config/custom_components/tuya_local/devices/`.
3. Restart Home Assistant.
4. Settings → Devices & Services → *Add Integration* → **Tuya Local**.
   Enter the four parameters below; the device is matched by its product ID and the
   bundled config supplies every entity automatically.

## Configuration parameters

```
host:              192.168.1.x        # your vacuum's LAN IP — reserve it in DHCP
device_id:         <your device id>
local_key:         <your local key>
protocol_version:  3.3
```

Both `device_id` and `local_key` are specific to *your* robot. Do not reuse anyone
else's, and do not commit your own values anywhere.

### Getting the local key

The vacuum has to be reachable on TCP 6668 first. Then:

- If the device is bound to a **Tuya IoT Platform** project of your own, the key is under
  *Cloud → API Explorer → Device Management → Query Device Details* (`local_key`).
- Devices paired through a **manufacturer-branded app** like Cecotec's do not appear in a
  Tuya developer account — they live in a partitioned cloud namespace. The usual remedy is
  to unpair from the brand app and re-pair into **Tuya Smart / Smart Life**, which puts the
  device in your account so the portal can show the key.

  Be aware of the trade-off: re-pairing issues a **new** local key and the brand app's
  map/cleaning features may not carry over.

Once you have it, verify before touching Home Assistant:

```python
import tinytuya
d = tinytuya.Device("<device_id>", "<ip>", "<local_key>", version=3.3)
d.set_socketTimeout(6)
print(d.status())   # expect {'dps': {...}}
```

## Supported features

The bundled config exposes 25 entities:

- **Vacuum** — start/pause, mode (Smart / Zone / Go to position), status, fan speed
  (gentle / normal / strong), locate, and manual direction control
- **Switches** — Charge, Do not disturb, Break clean, Auto dust collection, Customize mode,
  Auto boost, Y-shape mop mode
- **Selects** — Water level (low / medium / high)
- **Numbers** — Volume, Number of cleans, and the four consumable counters
  (edge brush, roll brush, filter, mop cloth)
- **Buttons** — Reset map, and a reset for each consumable
- **Sensors** — Cleaning time, cleaned area, battery
- **Binary sensors** — Fault, Mop installed

## Notes and known limits

- DP 4 offers only `smart`, `zone` and `pose`. There is no `spot`/`edges` mode on this
  model — do not copy the mode list from older Conga configs, it will not work.
- DP 28 (fault) is a bitmap that the device sends as a plain integer. The config types it
  as `bitfield`; `base64` looks similar in tuya-local but expects a string and will not
  decode this device. `tools/check_config.py` catches exactly this class of mistake.
- DP 40 is mop presence and is confirmed on this unit. DP 45 and 48 are booleans whose
  *type* is verified here but whose *function* is inherited from a same-generation device;
  both are marked optional and named from that source.
- Datapoints 49, 50, 51, 105, 120, 141, 144, 145, 147 and 148 also appear on this model and
  are deliberately left unmapped rather than guessed. `docs/dp-map.md` records the value
  each one held, so the next person has a starting point.
- Datapoints in the DP map that never appear in a status dump (10, 11, 12, 13, 14, 16, 18,
  20, 22, 24, 25, 26, 27, 32, 33, 34) are write-only function datapoints. That is expected.

## Related projects, and one trap

- **Congatudo** (`congatudo.cloud`, `congatudo/congatudo-add-on`) is a cloud replacement for
  Conga vacuums — but for the **3irobotix**-based ones (4690, 5090 and similar), *not* Tuya.
  It does not apply to the 11090. If you searched "Cecotec Conga Home Assistant" you almost
  certainly landed on it first.
- `alemuro/ha-cecotec-conga` and `arnimi/ha-cecotec-conga-1090-tuya` are **cloud**
  integrations (username/password) for the 5290/1090, not local control.
- Cecotec's `congas1970`, `congax70` and `congaz100` configs already in tuya-local are the
  same robot family but a **different DP generation**. Useful as a structural reference,
  not a drop-in. `docs/sweeper-dp-generations.md` explains the difference.
- When a product ID is missing from tuya-local entirely, a config for another brand on the
  same generation is often the right starting point.

## Contributing

Tested against firmware `3.5.53` (main and MCU modules). If your Conga reports a different
DP layout, open an issue with your `tinytuya` device status dump — that is enough to
reconcile the map.

The config belongs upstream in
`make-all/tuya-local/custom_components/tuya_local/devices/`. The template exists so that
adding another robot on this generation is mostly deleting lines.

## License

MIT
