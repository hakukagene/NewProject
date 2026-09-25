# Хулан — эхний өдөр

New Game now starts the supplied «Охин 1 (1)» story instead of the Eileen phone demo.
The original DOCX is not modified or committed. The source's main dialogue and
branch responses are adapted into native Ren'Py labels/menus in
`game/chapter_one.rpy`; state and screens live in `game/story_system.rpy`.

## Updating after the script rename

Keep only one copy of the chapter inside `game`. Ren'Py also loads orphaned
compiled scripts, so removing or renaming a source file alone may not remove
the duplicate at runtime.

Before pulling, back up any locally created `game/chapter_one.rpy` outside the
entire `game` directory. The repository now supplies that filename; keep local
edits in the backup for comparison instead of overwriting them.
After pulling, move any remaining `khulan_day_one.rpy`, `khulan_day_one.rpyc`,
`khulan_system.rpy`, and `khulan_system.rpyc` outside `game`. Do not keep backup
scripts in a subfolder of `game`, because Ren'Py scans those too.
Use Launcher → Force Recompile, removing orphaned compiled scripts when offered,
then start New Game. Existing chapter saves may refer to renamed labels/state
and are not guaranteed compatible. The earlier unrelated Sara mode is retained.

## Implemented flow

Future family framing → cafeteria and Anu's message → timed Saruul question →
classroom inspection and drawing incident → gazebo apology → chase → Khulan's
home and room inspection → family dinner → Badral's car → Bilguun's father →
Bolor desktop chat → Moment/Music browsing → comic dream → Day 2 teaser.

Menu captions without explicit dialogue in the source have authored response
lines. Relationship deltas are game-design additions, not numbers in the DOCX.
Each relationship is bounded 0–100. The source's main plot reconverges after
choices; scores and flags persist for a future Day 2, which is not yet written.
The dream is non-explicit: no nudity, voyeuristic photograph, or forced invasive
choice. Chingun's comic reveal is retained. All university characters are adults.

## Phone and chat

The chapter now opens an interactive phone for Anu's cafeteria message and a
desktop browser for the Bolor conversation. Desktop and phone share chat history,
drafts, music, notes and photos. See `docs/STORY_DEVICES.md` for navigation and
implementation details.

Story mode uses Bilguun's profile (52 followers / 52 following), Khulan, Anu,
Saruul, Chingun, and Bolor. Only Bolor uses live AI. Other contacts have a single
scripted reply, then remain read-only on the reply side. Likes do not farm trust.
The earlier Sara mode remains available to old saves (`story_active=False`).
For compatibility, the existing `sara` chat storage and transport keys are reused
for Bolor only in story mode; UI and server persona use Bolor's name.

Deploy the changed `backend/app.py` to the existing Render service to activate
the Bolor persona. Client requests send `character: bolor`; unknown/missing
characters keep the existing Sara persona. Existing boundary/relationship rules
still apply. No secrets, provider, API URL, or billing settings are changed.
Live replies require the configured Gemini service; offline failures stay visible.

## Story backgrounds and optional media

All 16 story locations now include generated environment artwork, exported as
1920×1080 WebP in `game/images/story/`. The existing scene loader selects each
image by scene ID. Night/dream and morning variants preserve the room layouts.
See `docs/BACKGROUND_PROMPTS.md` for the generation prompts and edit references.
Missing background files still fall back to solid colors.

Twelve temporary character assets now support the first visual test. Open
"Дүрийн тест" from the menu to browse them or turn story sprites off before
adding finished video scenes. See `docs/TEST_CHARACTERS.md` and
`docs/CHARACTER_PROMPTS.md` for usage and the prompt set.

Cover audio and reels remain optional. Posts fall back to title
cards, and unavailable audio is labeled.
Existing music library tracks remain playable. The YouTube reference was not
downloaded or redistributed.

Included scene artwork at `game/images/story/<scene_id>.webp` (1920×1080):
`family_future`, `cafeteria`, `corridor`, `classroom`, `school_gate`, `gazebo`,
`street_escape`, `khulan_gate`, `khulan_room`, `dinner`, `departure`, `police_car`,
`bilguun_home`, `bilguun_room`, `dream`, `day_two`.
Post artwork: `post_khulan.webp`, `post_anu.webp`, `post_saruul.webp`,
`post_chingun.webp` in the same folder. Cover audio: `game/audio/story/anu_cover.ogg`.
Reels are explicitly unavailable until authored video content is added.

## Verification

Run `python -m unittest discover -s tests -v` and, after installing backend
requirements, `python -m unittest discover -s backend -v`.
Before release, run Ren'Py 8.5.3 Check Script/Lint and play the chapter: test timed
choice timeout/manual selection, every inspection item, positive/negative choices,
save/load/rollback, Bolor success/offline/block, phone exit, and Day 2 end screen.
Engine-independent tests cannot establish visual or runtime correctness.

Implementation checks: 7 story-state tests and 13 backend tests passed. Ren'Py
8.4.1 SDK lint was also run on the complete project. A visual playthrough on the
target 8.5.3 engine and live Render/Gemini verification are still required.
