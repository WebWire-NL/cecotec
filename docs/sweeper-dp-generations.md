# Sweeper datapoint generations

Tuya robot vacuums do not all use the same datapoint layout. This is the map of
which layouts are in circulation, so you can tell in one dump which template your
robot needs.

Derived by surveying the **50 vacuum configs in the public tuya-local corpus**
(September 2026). The datapoints quoted are those on the `vacuum` entity only —
the configs also carry their own config and diagnostic entities.

## A — standard sweeper

```
vacuum datapoints:  1, 2, 4, 5, 9, 11, 12   (optional extras 14, 16, 28, 32-35)
```

The layout this repo targets. If your dump has datapoints 1 (`power`) and 5
(`status`) and 9 (`fan_speed`) together, you are almost certainly here.

| brand | model | config |
|---|---|---|
| Cecotec | Conga 11090 Spin Revolution Home&Wash | **this repo** |
| Cecotec | Conga X70 | `cecotec_congax70_vacuum.yaml` |
| ABIR | X8, X9 | `abir_x8_vacuum.yaml`, `abir_x9_vacuum.yaml` |
| Gadnic | AC800 | `gadnic_ac800_vacuum.yaml` |
| ILIFE | A12 Pro, A30 Pro, V20, V30 | `ilife_*_vacuum.yaml` |
| Kabum | Smart 700 (2023) | `kabum_smart700_v2023_vaccum.yaml` |
| Liectroux | XR500 T3 | `liectroux_xr500_t3_vacuum.yaml` |
| Lublueblu | SL60D | `lublueblu_sl60d_vacuum.yaml` |
| Medion | X10SW | `medion_x10sw_vacuum.yaml` |
| Neatsvor | X600 | `neatsvor_x600_vacuum.yaml` |
| Rowenta | X-plorer 75S | `rowenta_xplorer75s_vacuum.yaml` |
| Siguro | TurboVac Navigator | `siguro_turbovacnavigator_vacuum.yaml` |
| Tesvor | S6 | `tesvor_s6_vacuum.yaml` |
| Ttec | Reobi Pro | `ttec_reobipro_vacuum.yaml` |

Template: [`templates/tuya_sweeper_standard_a.yaml`](../templates/tuya_sweeper_standard_a.yaml)

## B — high-id generation

```
vacuum datapoints:  101, 102, 104, 105, 109, 111, 112, 123-132
```

Nothing on low datapoint numbers. Different firmware line entirely — do not try to
adapt generation A to it.

| brand | model |
|---|---|
| Kogan | LX8, LX10, LX15 |
| Liectroux | G7 |
| Realme | TechLife |
| Tefal | X-plorer |

## C — low-id alternate

```
vacuum datapoints:  2, 3, 4, 5, 13, 14
```

Datapoint 3 carries the **command** here, where generation A puts `charge` on 3
and the command on 4. Easy to confuse with A at a glance; check datapoint 4.

| brand | model |
|---|---|
| Cecotec | Conga S1970 |
| Airrobo | P20 |
| Honiture | G20, Q6 Pro |
| iHome | AutoVac Nova |
| Kabum | Smart 700 |
| Lefant | M213, T700 |
| Mamnv | BR151 |
| Medion | S10, S20 |
| OKP | K2 |
| Rinkmo | D2 |
| Ultenic | T10 |

## D — everything else

Individually-shaped layouts, one or two configs each. No template; start from the
closest one and check every datapoint.

`cecotec_congaz100`, `blaupunkt_xboost`, `kabum_smart500`, `kyvol_e30`,
`laresar_l6nex`, `lefant_ls1`, `lefant_n3`, `lenovo_e1`, `lubluelu_a901`,
`mellerware_citymove`, `parkside_ppwd30a1` (a workshop vacuum, not a robot),
`proscenic_850t`, `proscenic_m9`.

## Telling them apart

Dump your device and read the keys:

```python
import tinytuya, json
d = tinytuya.Device("<device_id>", "<ip>", "<local_key>", version=3.3)
d.set_socketTimeout(6)
print(json.dumps(d.status().get("dps", {}), indent=1, sort_keys=True))
```

- `1` and `9` and `11` present, nothing above 200 → **A**
- only ids in the 100s → **B**
- `4` looks like a status and `3` looks like a command → **C**
- anything else → **D**

Then check your config against that dump:

```
python3 tools/check_config.py --config templates/tuya_sweeper_standard_a.yaml --dump dump.json
```
