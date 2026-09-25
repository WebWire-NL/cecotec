# Cecotec Conga 11090 Spin Revolution Home&Wash — Home Assistant (local)

Local (cloud-free) Home Assistant support for the **Cecotec Conga 11090 Spin Revolution
Home&Wash** robot vacuum. The robot is a Tuya device behind Cecotec's branded app, so once
you have its local key it talks plain Tuya LAN protocol on port 6668.

Product ID: `kazdsquasfw0gmrn` · category `sd` · Tuya protocol **3.3**

## What's in here

| Path | What it is |
|---|---|
| `devices/cecotec_conga_11090_vacuum.yaml` | Device config for [tuya-local](https://github.com/make-all/tuya-local) — 22 entities |
| `docs/dp-map.md` | Full DP map (34 datapoints, names, types, value ranges) |

The DP map was not guessed. It follows the Tuya standard sweeper layout (category
`sd`), and every datapoint and value range in it was confirmed against what the
vacuum itself reports on the LAN.

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

The bundled config exposes:

- **Vacuum** — start/pause, mode (Smart / Zone / Go to position), status, fan speed
  (gentle / normal / strong), locate, and manual direction control
- **Switches** — Charge, Do not disturb, Break clean, Auto dust collection, Customize mode
- **Selects** — Water level (low / medium / high)
- **Numbers** — Volume, Number of cleans, and the four consumable counters
  (edge brush, roll brush, filter, mop cloth)
- **Buttons** — Reset map, and a reset for each consumable
- **Sensors** — Cleaning time, cleaned area, battery
- **Binary sensor** — Fault

## Notes and known limits

- DP 4 offers only `smart`, `zone` and `pose`. There is no `spot`/`edges` mode on this
  model — do not copy the mode list from older Conga configs, it will not work.
- The robot also emits vendor-specific datapoints outside the standard schema
  (40, 45, 48, 49, 50, 51, 105, 120, 141, 144, 145, 147, 148 — mop presence, carpet
  behaviour, cleaning result and similar). They are deliberately left out of the config
  rather than mapped on a guess. Extend it if you work out what they do.
- DP 28 (fault) is a bitmap; the config exposes it as a plain problem binary sensor.

## Related projects, and one trap

- **Congatudo** (`congatudo.cloud`, `congatudo/congatudo-add-on`) is a cloud replacement for
  Conga vacuums — but for the **3irobotix**-based ones (4690, 5090 and similar), *not* Tuya.
  It does not apply to the 11090. If you searched "Cecotec Conga Home Assistant" you almost
  certainly landed on it first.
- `alemuro/ha-cecotec-conga` and `arnimi/ha-cecotec-conga-1090-tuya` are **cloud**
  integrations (username/password) for the 5290/1090, not local control.
- Cecotec's `congas1970`, `congax70` and `congaz100` configs already in tuya-local are the
  same robot family but a **different DP generation**. Useful as a structural reference,
  not a drop-in.
- The Tuya standard sweeper DP layout is shared across rebadges — ILIFE, ABIR, Neatsvor,
  Proscenic, Medion, Liectroux, Rowenta, Kogan, Kabum, Blaupunkt, Ttec, Gadnic and others
  ship the same dp1/2/4/5/9/11/12 semantics. When a product ID is missing from tuya-local,
  a config for another brand is often the right starting point.

## Contributing

Tested against firmware `3.5.53` (main and MCU modules). If your Conga reports a different
DP layout, open an issue with your `tinytuya` device status dump — that is enough to
reconcile the map.

To upstream this, the config belongs in
`make-all/tuya-local/custom_components/tuya_local/devices/`.

## License

MIT
