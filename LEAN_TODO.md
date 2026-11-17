# renpy-lean status

Bare-bones Ren'Py project: `game/script.rpy`, the default Ren'Py UI files (`options`, `gui`, `screens`), `game/scripts/image/{char,backgrounds}.rpy`, `game/scripts/CORE/special_effects.rpy`, and the assets (`images`, `audio`, `gui`, `fonts`). All systems, HUD, walking, caches and junk are removed (still in git history on `renpy`).

## Changes made to script.rpy
- Removed player/inventory/missions setup, `show/hide screen` calls, movement and `move_to_pos`.
- Added `default inventory = []` so the existing `inventory.append(...)` lines work.
- Walk-around opening replaced by a 3-option `menu` (front seat / back seat / ask sergeant again). Dialogue lines are unchanged.
- `screens.rpy`: main menu background is now `gui.main_menu_background`.

## Ren'Py lint (SDK 8.x) shows these existed before the cleanup
1. `jump fixprojectoralone` (script.rpy ~line 653): label does not exist. That route is missing.
2. Characters used but never defined: `RAM` (42 lines), `KNIGHT` (17), `RED_HOOD` (16). `Sultan` is defined as `SUL`.
3. 133 `scene`/`show` names that are not images (`bg_elevator`, `ben_neutral`, `samuel_normal_pose`, `bagman_default`, `drill_sarg_talk`, ...). The first screens of the script resolve; most of the second half does not.
4. Duplicate `default preferences.text_cps` (script.rpy:5 and options.rpy), duplicate `define MAR` in char.rpy.
5. `_alt` duplicate labels (around lines 650-1000) are likely dead copies.
6. `options.rpy` still says name "Reflection" and a `TheMerge-...` save directory.
7. `game/audio/player` (about 378 MB of TTS voice files such as Debate Host and Meowbahh) is not referenced by the script. Left in place; delete if it belongs to another project.

Run lint with: `D:\renpy\renpy-8.0.1-sdk\renpy.exe D:\wre\Projection-renpy-lean lint`
