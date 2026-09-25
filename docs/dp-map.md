# DP map — Cecotec Conga 11090 Spin Revolution Home&Wash

Product ID: `kazdsquasfw0gmrn`  ·  category: `sd`

Tuya standard sweeper layout (category `sd`); every entry confirmed against the device's own LAN status output.
`RW` = writable in the app (has a function code); `RO` = status only.

| DP | standard code | app code | type | range | R/W |
|---|---|---|---|---|---|
| 1 | `power_go` | `switch_go` | Boolean | — | RW |
| 2 | `pause` | `pause` | Boolean | — | RW |
| 3 | `switch_charge` | `switch_charge` | Boolean | — | RW |
| 4 | `mode` | `mode` | Enum | smart, zone, pose | RW |
| 5 | `status` | — | Enum | standby, zone_clean, part_clean, cleaning, paused, goto_pos, pos_arrived, pos_unarrive, goto_charge, charging, charge_done, sleep | RO |
| 6 | `clean_time` | — | Integer | 0..9999 min | RO |
| 7 | `clean_area` | — | Integer | 0..9999 ㎡ | RO |
| 8 | `electricity_left` | — | Integer | 0..100 % | RO |
| 9 | `suction` | `suction` | Enum | gentle, normal, strong | RW |
| 10 | `cistern` | `cistern` | Enum | low, middle, high | RW |
| 11 | `seek` | `seek` | Boolean | — | RW |
| 12 | `direction_control` | `direction_control` | Enum | forward, backward, turn_left, turn_right, stop | RW |
| 13 | `reset_map` | `map_reset` | Boolean | — | RW |
| 14 | `path_data` | `path_data` | Raw | — | RW |
| 15 | `command_trans` | `command_trans` | Raw | — | RW |
| 16 | `request` | `request` | Enum | get_map, get_path, get_both | RW |
| 17 | `edge_brush` | — | Integer | 0..9000 min | RO |
| 18 | `reset_edge_brush` | `edge_brush_life_reset` | Boolean | — | RW |
| 19 | `roll_brush` | — | Integer | 0..18000 min | RO |
| 20 | `reset_roll_brush` | `roll_brush_life_reset` | Boolean | — | RW |
| 21 | `filter` | — | Integer | 0..9000 min | RO |
| 22 | `reset_filter` | `filter_reset` | Boolean | — | RW |
| 23 | `duster_cloth` | — | Integer | 0..9000 min | RO |
| 24 | `reset_duster_cloth` | `rag_life_reset` | Boolean | — | RW |
| 25 | `switch_disturb` | `do_not_disturb` | Boolean | — | RW |
| 26 | `volume_set` | `volume_set` | Integer | 0..100 % | RW |
| 27 | `break_clean` | `break_clean` | Boolean | — | RW |
| 28 | `fault` | — | Bitmap | bitmap: lidar_shelter, wheel_up, low_battery, dust_water, ground_start, cliff_ir... | RO |
| 32 | `device_timer` | `device_timer` | Raw | — | RW |
| 33 | `disturb_time_set` | `disturb_time_set` | Raw | — | RW |
| 34 | `device_info` | — | Raw | — | RO |
| 37 | `dust_collection_num` | `dust_collection_num` | Integer | 0..4 | RW |
| 38 | `dust_collection_switch` | `dust_collection_switch` | Boolean | — | RW |
| 39 | `customize_mode_switch` | `customize_mode_switch` | Boolean | — | RW |
