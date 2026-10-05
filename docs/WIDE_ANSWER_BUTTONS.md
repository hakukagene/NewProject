# Wide answer buttons

All standard story menus and both timed-choice screens use the approved concept 04: a wide vertical list above the dialogue area, translucent brown idle buttons, thin gold borders, and gold hover fill with dark text.

The shared screen lives in `game/wide_choices.rpy`. Desktop width is 1380, minimum button height 64, text size 28, and spacing 12 in the 1920×1080 coordinate space. The small variant uses width 1560, minimum height 76 and text size 32. The list is anchored above the configured dialogue area. Long captions wrap and increase button height; exceptionally tall lists scroll by wheel or drag.

Captions and actions pass through directly. No chapter dialogue or answer text was changed, shortened, or regenerated. The existing timed-choice heading, countdown duration, option ordering and timeout return are preserved. This branch starts from the user's `724b6c2` text edit.

Validation: Ren'Py 8.4.1 lint and diff checks; rendered short, long and timed answer lists; width branch for small displays rendered; timed-choice expiry returns the original final-option index. The preview harness was removed. A physical mobile device was not tested.
