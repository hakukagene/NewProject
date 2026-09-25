# First-test character stills

Twelve generated assets are included under `game/images/characters/test/`.
Each is a 1024×1536 WebP with real alpha, exported losslessly from the generated
PNG. The original generation prompts are in `CHARACTER_PROMPTS.md`.

Open **Дүрийн тест** from the main or pause menu to preview any character on four
backgrounds. The toggle controls whether these temporary sprites appear in the
chapter. It defaults to on and persists between sessions. Turning it off hides
the stills immediately, including when returning from the pause menu.

Chapter scene changes set a provisional cast with up to four assets visible at
once. The crowd arrival, mother's entrance and Chingun's dream reveal update the
cast at their corresponding story beats. Phone and desktop screens stay above
the sprites. Anu and Bolor are available in the gallery rather than standing in
Bilguun's room while communicating remotely.

These are static visual stand-ins, not animations or completed video scenes.
There is one basic pose/expression per character. The opening family frame uses
the same provisional Bilguun/father designs; older-time-period variants are not
included. Dinner and car scenes use standing test sprites rather than final
seated blocking. The lecturer's appearance and unspecified clothing/ages are
design assumptions for this first test.

For video production, turn off the test-art toggle. The story placements are
isolated behind `story_set_test_cast()` / `story_set_test_actors()` calls and
`game/story_test_characters.rpy`; remove those calls and the temporary gallery
when the finished video sequence replaces this prototype. Existing video files
are not modified.

Validation: all 12 assets decode with alpha at 1024×1536; 13 existing tests pass;
Ren'Py 8.4.1 lint passes. Engine renders checked the two/four-actor layouts,
gallery and disabling the stills. Preview screenshots are in
`previews/character-scene.png` and `previews/character-gallery.png`.
