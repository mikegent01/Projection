# Projection — Core Systems Review

> Status: **DRAFT — for discussion.** For each system below, mark a decision:
> ✅ **KEEP** (as-is) · 🔧 **REFINE** (keep, but rework) · ❌ **REMOVE** (cut it) · ❓ **UNDECIDED**
>
> Goal of this pass: agree on the final list of systems, then do the cleanup/refactor in follow-up commits on this PR (or separate PRs per system).

---

## 1. Inventory of Systems

### A. Character / RPG Core

| # | System | Where it lives | Size | Decision |
|---|--------|----------------|------|----------|
| A1 | **GameCharacter class** (stats, XP/leveling, emotions, health, relationships, sanity) | `scripts/CORE/classes.rpy` | ~300 lines | ❓ |
| A2 | **Inventory class** (weight, durability, equip slots, breakage) | `scripts/CORE/classes.rpy` (bottom half) | ~200 lines | ❓ |
| A3 | **Skill roll system** (d100 rolls, thresholds, proficiency auto-detection, roll history queue) | `classes.rpy` (`perform_roll`) + `rolls.rpy` (roll history screen) | ~150 lines | ❓ |
| A4 | **Proficiency sub-skill system** (per-stat proficiencies with their own XP/levels, energy costs) | `classes.rpy` + `player.rpy` | ~100 lines | ❓ |
| A5 | **Emotion system** (7 emotions, each granting stat bonuses/penalties, top-5 weighted scaling into rolls) | `classes.rpy` (`_get_emotion_bonus`, `modify_emotion`) + `player.rpy` | ~80 lines | ❓ |
| A6 | **Per-body-part health** (6 parts × health/conditions/temperature/cleanliness; head=0 → game over) | `classes.rpy` + `screens/health_status.rpy` (793 lines of UI) | large | ❓ |
| A7 | **Temperature & cleanliness simulation** (cleanliness shifts temperature, room temp with random variation, hypothermia/overheating conditions) | `classes.rpy` | ~60 lines | ❓ |
| A8 | **Relationships** (trust/friendship/hostility per NPC, descriptor tiers) | `classes.rpy` (hardcoded Samuel/Barns in `__init__`) | ~40 lines | ❓ |
| A9 | **Sanity** | `classes.rpy` — defined (`self.sanity = 100`) but **never used anywhere** | 1 line | ❓ |
| A10 | **Energy costs on proficiencies** | `player.rpy` — `energy_cost` values defined, but **no energy stat exists to spend** | data-only | ❓ |

### B. Survival / Interaction Systems

| # | System | Where it lives | Size | Decision |
|---|--------|----------------|------|----------|
| B1 | **Item database** (weapons/tools/junk, weight, durability, repairable) | `scripts/systems/items.rpy` | 127 lines | ❓ |
| B2 | **Crafting / combining** (2-item recipes + deconstruction recipes) | `scripts/systems/crafting.rpy` + screens in `inventory_screen.rpy` **and again** in `mixing.rpy` | duplicated | ❓ |
| B3 | **Liquid system** (containers, pouring, draining, ml amounts) | `scripts/systems/liquid.rpy` (mostly placeholder stubs) | 398 lines | ❓ |
| B4 | **Liquid mixing + stirring minigame** (mix recipes, directional stirring, progress) | `scripts/systems/mixing.rpy` (a "merged file" that re-implements liquid.rpy) | 702 lines | ❓ |
| B5 | **Medical treatment** (medkit items → cure conditions, healing timers, confirmation flow) | `crafting.rpy` (`medkit_contents`) + `health_status.rpy` + `inventory_screen.rpy` | spread across 3 files | ❓ |
| B6 | **Equipment slots** (head/body/arms/hands/legs item slots) | `classes.rpy` (Inventory.equip) + globals in `CORE/inventory.rpy` **and duplicated** in `super_important.rpy` | duplicated | ❓ |
| B7 | **2D movement / platforming** (WASD + jump, gravity, 8-direction mouse-facing sprites) | `scripts/CORE/movement.rpy` | 152 lines | ❓ |
| B8 | **Look/inspect hotspots** (proximity-gated "look at" screens per object) | `scripts/screens/look.rpy` | 205 lines | ❓ |
| B9 | **Talk system** (speak-to-people overlay) | `scripts/screens/talk.rpy` | 38 lines | ❓ |
| B10 | **Minigames** | `scripts/systems/minigame.rpy` is **empty (0 lines)**; old compiled `minigames.rpyc.bak` lingers | dead | ❓ |

### C. Narrative / Meta Systems

| # | System | Where it lives | Size | Decision |
|---|--------|----------------|------|----------|
| C1 | **Journal & missions** (entries, active/completed missions with progress %) | `scripts/systems/journal.rpy` + `HUD.rpy` — **conflicting storage**: `persistent.*` in some places, plain `default` vars in others | split-brain | ❓ |
| C2 | **Books / readable documents** (unlock, paginated reader at 250 words/page) | `journal.rpy` + `HUD.rpy` (`read_book_screen`) + `game/books/` | medium | ❓ |
| C3 | **Collected tapes** (audio tapes tab in journal) | `journal.rpy` + `HUD.rpy` | small | ❓ |
| C4 | **In-world papers** (SCP memo, network notice, Vatican newspaper, "cuz" document) | `scripts/screens/papers.rpy` | 677 lines | ❓ |
| C5 | **Radio** (modes, volume, battery drain, per-label track lists) | `scripts/screens/radio.rpy` | 182 lines | ❓ |
| C6 | **Game state dict** (chapter flags, projector status/health — projector 0 HP = game over) | `scripts/CORE/chapter1.rpy` (`game_state`) | 23 lines | ❓ |
| C7 | **HUD** (bottom bar, stage curtains, tutorial overlay) | `scripts/screens/HUD.rpy` | 522 lines | ❓ |
| C8 | **Random title screens** (4 title screens, each with own music pool) | `scripts/CORE/title_ui.rpy` | 22 lines | ❓ |
| C9 | **Special effects** (dim overlay, light-flick effect, custom dimming layer) | `scripts/CORE/special_effects.rpy` — note: `light_turning_on_effect` is **defined twice**, second silently wins | 30 lines | ❓ |
| C10 | **Roll history overlay** (scrollable last-15-rolls panel) | `rolls.rpy` | 43 lines | ❓ |

---

## 2. The Mess: Concrete Problems Found

These are issues regardless of which systems we keep — the ones marked 🔥 actively break or corrupt behavior.

### 🔥 Blocking / behavior bugs
1. **Game currently crashes** — `errors.txt`/`traceback.txt`: `scene walkaway1 at fit_screen` fails because `backgrounds.rpy:220` has a trailing `xysize (...)` line inside the previous image block, which breaks parsing of `transform fit_screen` right below it (line 234 ATL error).
2. **Journal/missions storage is split-brain** — `HUD.rpy` uses `persistent.journal_entries`, `journal.rpy` defines a *separate* non-persistent `journal_entries` + `missions`, and `super_important.rpy` initializes the persistent ones. Entries will appear/disappear depending on which code path touched them, and persistent data leaks across save slots.
3. **Duplicate screen definitions with conflicting logic** — `character_status_screen` is defined **3×** (`inventory_screen.rpy`, `liquid.rpy`, `mixing.rpy`), `crafting_screen` **2×**, and functions `add_liquid`/`remove_liquid`/`mix_liquids`/`has_stirring_tool`/`select_item` are each defined in 2–3 files. Whichever file loads last wins — silent, load-order-dependent behavior.
4. **`mixing.rpy` is a literal merge dump** — its header says "Combined File: Merged scripts…". It duplicates ~all of `liquid.rpy` plus crafting screens. One of the two must go.
5. **`super_important.rpy` duplicates `CORE/inventory.rpy`** verbatim (the 8 equipment-slot globals) and is otherwise a grab-bag (persistent init, label callback, keybind surgery, `gameover` label).
6. **Shared mutable defaults** — `player` and `barns` are both constructed from the *same* `player_initial_stats` / `player_initial_proficiencies` dicts. `GameCharacter.__init__` stores the reference, so leveling Benjamin's strength also levels Barns's. Same for relationships being hardcoded inside the class.
7. **`special_effects.rpy`** defines `light_turning_on_effect` twice — the first version is dead code.

### 🧹 Repo hygiene
8. **81 `.bak` files and 4 `.rpyc` files are committed** (`gui.rpy.1.bak`, `screens.rpy.1.bak`, every GUI png `.1.bak`, `scripts/*.rpyc.bak`…). The `.gitignore` covers `*.rpyc` but these were committed before it took effect.
9. **`game/saves/` is committed** (navigation.json, persistent) despite `**/saves/` in `.gitignore`.
10. **Log/debug artifacts committed**: `errors.txt`, `log.txt`, `traceback.txt`, `progressive_download.txt` at repo root (`.gitignore` lists them, but they're already tracked).
11. **Dead files**: `scripts/systems/minigame.rpy` (0 bytes), `scripts/CORE/ui_s.rpy` (5 lines), `.rpyc.bak` files for deleted scripts (`interaction_overlay`, `look`, `minigames`, `talk`).
12. **Monolithic `script.rpy` (1,439 lines)** with heavily duplicated branches (`getuniformwithsamuel` vs `getuniformwithsamuel_alt`, `process_weapon_choice` vs `_alt` vs `_alone2` — near-identical copies).

### 🧟 Half-built / orphaned features (decide: finish or cut)
13. **Sanity** (A9) — one line, never read or written elsewhere.
14. **Energy costs** (A10) — data exists, no energy pool or spending logic.
15. **Liquid system stubs** (B3) — `drain_liquid`, `pour_liquid`, `mix_liquids`, `reset_stirring` are `renpy.notify` placeholders; `has_stirring_tool` always returns `True` ("for testing").
16. **`nenvershowrolls`** (typo'd flag controlling roll popups) — presumably meant `never_show_rolls`, and its logic is inverted vs. its name.
17. **Backgrounds file self-labels temp code**: "200 Lines will be removed at the end of this".

---

## 3. My Recommendations (starting point for discussion)

**Strong keeps (core identity of the game):**
- A1 GameCharacter, A3 rolls, A6 body-part health, B1 items, B5 medical, C1 journal/missions (after fixing storage), C4 papers, C5 radio, C7 HUD — these fit the "disaster survival VN" premise and are mostly functional.

**Refine (keep the idea, rebuild the code):**
- **B2/B3/B4 crafting + liquids** → collapse `mixing.rpy` and `liquid.rpy` into ONE system file + ONE screen file; delete duplicate screens/functions. This is the single biggest source of mess.
- **A2 Inventory + B6 equipment** → keep the class, delete the loose `*_item` globals (`CORE/inventory.rpy` + duplicate in `super_important.rpy`); slots already live in the Inventory class.
- **A5 emotions** → the top-5 weighted bonus math is clever but opaque and hard to tune/debug. Consider simplifying to "highest emotion gives its bonus."
- **A8 relationships** → move out of `__init__` hardcoding into data (`default` dicts), so new NPCs don't require class edits.
- **C6 game_state** → fine as a concept; grow it as the flag store instead of scattering new `default`s.
- **script.rpy** → split per-chapter, and deduplicate the `_alt` label copies with parameters/flags.

**Candidates to cut (unless you have near-term plans):**
- **A7 temperature/cleanliness sim** — high complexity, invisible to the player, and it silently mutates conditions via random variation. Cut or shelve until the survival loop needs it.
- **A9 sanity, A10 energy** — delete the dead lines/data now; re-add when designed.
- **B7 2D movement** — a platformer engine inside a VN is a huge maintenance tax for one walking segment. Keep only if walking sections are a core pillar; otherwise replace with point-and-click hotspots (B8 already does this well).
- **B10 minigame.rpy** — empty file, delete.
- **A4 proficiencies** — *borderline.* Stats + proficiencies + emotions + circumstance is 4 stacked modifier layers on every roll. Consider folding proficiencies into flat stat bonuses until the game is longer.

**Repo hygiene (no gameplay impact — can do immediately once you say go):**
- `git rm` all `.bak`, `.rpyc`, `saves/`, and root log files (they're already gitignored, just still tracked).
- Fix the `fit_screen` parse error so the game runs again.
- Fix the journal persistent/store split-brain.

---

## 4. Decision Table (fill this in)

| System | Keep / Refine / Remove | Notes |
|--------|------------------------|-------|
| A1 GameCharacter | | |
| A2 Inventory class | | |
| A3 Skill rolls | | |
| A4 Proficiencies | | |
| A5 Emotions | | |
| A6 Body-part health | | |
| A7 Temp/cleanliness | | |
| A8 Relationships | | |
| A9 Sanity | | |
| A10 Energy costs | | |
| B1 Item database | | |
| B2 Crafting | | |
| B3 Liquids | | |
| B4 Mixing/stirring | | |
| B5 Medical | | |
| B6 Equipment slots | | |
| B7 2D movement | | |
| B8 Look hotspots | | |
| B9 Talk | | |
| B10 Minigames | | |
| C1 Journal/missions | | |
| C2 Books | | |
| C3 Tapes | | |
| C4 Papers | | |
| C5 Radio | | |
| C6 game_state | | |
| C7 HUD | | |
| C8 Title screens | | |
| C9 Special effects | | |
| C10 Roll history | | |
