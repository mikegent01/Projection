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
7. `game/audio/player` (unused TTS voice files referencing real people/memes) deleted. Unused meme Character defs (Baldi, Jesus, Meowbahh, Marc) removed from char.rpy.

Run lint with: `D:\renpy\renpy-8.0.1-sdk\renpy.exe D:\wre\Projection-renpy-lean lint`

## IP cleanup still to do (decision: original IP, no SCP/real references)
- Rename "AAXA SCP-A01/A02", "this SCP" (script.rpy lines 156, 559, 615, 872, 928, 1082, 1099) once the organization name is chosen.
- Review: DARPA (261), Nu-7 (1313, 1386), "the foundation"/dod (1092), Butts2012 (602, 915), K-pop earphones (392, 705).
- Ending: the other-world material is not in this script (it ends at the osprey briefing); gut it in the Twine draft/bible only.
