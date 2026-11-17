# renpy-lean: what still needs changing

Branch `renpy-lean` (from `renpy`). The system files were deleted; `game/script.rpy` is untouched, so the game will not launch until the items below are handled. Nothing was rewritten.

## Deleted
`scripts/systems/*` (crafting, items, journal, liquid, mixing, minigame), `screens/{health_status,inventory_screen,inventory_style,papers,radio,look,talk}.rpy`, `CORE/{classes,inventory,player,rolls,movement,ui_s}.rpy`.

## Still present but bloat (delete once script no longer calls it)
- `scripts/screens/HUD.rpy`: all inventory/journal HUD except `screen stagecurtians()` (line 128), which the script shows.
- `scripts/CORE/chapter1.rpy`: `game_state` dict, used only by the walk-around section.
- `scripts/CORE/super_important.rpy`: persistent missions/rolls setup; `label gameover` is worth keeping.
- `scripts/CORE/title_ui.rpy`, `scripts/image/backgrounds.rpy` screens `samuel`/`drill_sargent` (line 230+): check what they do.

## `game/script.rpy` lines that reference deleted systems
| Lines | What | Suggested handling |
|---|---|---|
| 6-10 | `player.apply_room_temperature`, `player.inventory.add_item` | remove |
| 12-24 | `missions[...]` | remove |
| 26-30 | `show screen stagecurtians/samuel/drill_sargent/game_screen`, `movement_enabled` | keep stagecurtians/samuel/drill_sargent only if they are just images; drop `game_screen` |
| 120-121, 157-159, 204-206 | `show/hide screen checkKey, HUD, tutorial_screen` | remove |
| 123-155 | `label intreactivesection01` + `DrillSergeantTalk`: walk-around exploration (needs `movement`, `look` screens, `game_state`) | DECISION: replace with a plain `menu` (front seat / back seat / talk to sergeant) |
| 208 | `move_to_pos(130,450)` | remove |
| 359, 473, 583, 786, 896, 1098, 1212, 1267, 1418 | `inventory.append(...)` | remove, or turn into plain `default` flags if later text depends on the item |
| 441-450, 754-763, 1235-1241, 1418 | `player_weapon_choice` | keep as a normal variable (works without systems) |

## Script problems found (not blockers)
- `_alt` duplicate labels (e.g. `getuniformwithsamuel_alt`, `getscrewdriverwithsamuel_alt`, `abandonsamuel_alt`, around lines 694-1000): dead duplicates, no `jump` should reach them. Verify, then delete or merge.
- `process_weapon_choice` is reused by the `_alt` branch (see the comment at line 755).
- `config.name` is still "Reflection" and `save_directory` is "TheMerge-..." in `options.rpy`.

## Assets
Art is NOT copied. Newer art lives in `unity/Projection/Assets/images` (master) and the archive at `D:\GameDONOTDELETE`. The script's image names (`scene stage1`, `bg_outside_projector_room`, `ben neutral`...) come from `scripts/image/*.rpy` and `game/images/`; confirm each one exists before first launch. `.bak` files and `game/audio/player/*.zip` are junk still to remove.
