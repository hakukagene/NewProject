# October 2 screenplay additions

The revised screenplay inserts a night conversation and a new day before the existing classroom crisis. Chapter two now calls `story_october_night` and `story_october_day_three`; the previous next-morning scene becomes day four. Existing choice identifiers remain unchanged so saved choice state keeps its meaning.

Added content:

- The scripted second conversation with Bolor appends to existing messages once. It preserves relationship state and does not append when blocked, at four strikes, or in an active cooldown. The existing AI chat remains available when allowed.
- Anu's complete farewell arrives in the desktop message thread. Her final cover is the first Moment post; Khulan's flower story is available in the phone feed/story view. Both desktop and phone use the same save-backed feed selection.
- The school noticeboard, parking-lot assault, Saruul's intervention, hospital trip, accidental disclosure of Bilguun's name, and an unknown observer taking a photograph.
- The siblings' video call is described in the dialogue; the leaking sink, repair, change of shirt, and Saruul's parting conversation follow.
- Khulan waits outside Bilguun's home. The source contains no conversation at this point, so none is invented; play transitions to the following morning.

There are ten new four-option choice groups (`oct02_choice_1` through `oct02_choice_10`) with the supplied conditional replies. Six timed W/A/S/D prompts support keyboard input and clickable/touch buttons. Correct answers are counted and saved; mistakes and timeouts always continue. The story outcome remains the screenplay's two opponents down followed by the group overpowering Bilguun, regardless of QTE score.

The sink scene names Chingun once even though the surrounding scene follows Bilguun. This apparent typo is corrected to Bilguun. A word split across source paragraphs is rejoined. No new relationship score effects are invented for these choices.

## Assets and compatibility

Final video/audio is not included in the upload. New `school_parking`, `saruul_car`, and `hospital_exterior` locations use the existing neutral background fallback, as does `saruul_home` from the previous update. Existing character stills remain in use. Add matching `.webp` files under `game/images/story/` to replace these backdrops. The final cover has its own optional `audio/story/anu_farewell.ogg` playback controls; without that file the feed explicitly indicates that the recording is pending. It does not reuse the previous cover as if it were a new recording.

A save already beyond the inserted night will not replay the additions automatically. Start a new game or load before the second night's computer scene to see the complete sequence. No backend deployment is required for this update.

## Validation

Ren'Py 8.4.1 lint passed. Four automated chapter-two traversals exercised all new A/B/C/D choices, retained the original twenty choice groups, reached day four, and completed the chapter. The actual QTE screen received queued correct, wrong, mixed, and no-input events, yielding scores 6, 0, 3, and 0 respectively. Chat seeding was checked for normal, blocked, strike-limit, and cooldown states and for duplicate calls. Device/inspection screens were automatically dismissed only in that traversal harness. Separate runs rendered the actual phone feed, desktop feed, and QTE for visual inspection. Temporary test harnesses are not shipped. No live model call or mobile-device test was performed.
