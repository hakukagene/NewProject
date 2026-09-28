# Gold Tabs menu system

Applies approved concept 04 to the main menu, Settings, Save/Load, History, Gallery, About, Help, confirmation prompts, choice buttons, quick controls and transient notices. In-story phone/desktop application layouts are not game menus and remain independent.

`game/gold_menus.rpy` owns shared top tabs, gold selection diamond, serif headings, warm translucent cards, footer controls, switches, radio buttons, sliders and menu scrollbars. `screens.rpy` keeps the existing Ren'Py save/load/history/help actions inside the new shell. Gallery retains character/background selection and the persistent test-art toggle. Main menu has three matching New Story / Continue / Explore cards. Continue remains disabled without a save; Save/History tabs are disabled in the main-menu context.

All coordinates are on the existing 1920×1080 game canvas. The same composition scales with the game window. Native Ren'Py controls provide mouse, keyboard and touch interaction; menu text is not baked into the background.

Artwork: `game/gui/gold/desk.webp`, built-in ImageGen edits of concept 04. Prompt: remove overlay text, panels, controls and gold rules while preserving the desk composition, lighting, notebook, cup, earphones and window; restore the phone at the original position using the approved desk reference. No university names. SVG panel and control assets are code-authored. Existing bundled DejaVu Serif/license is reused.

Validation: Ren'Py 8.4.1 lint passes. Actual software-renderer screenshots were inspected for main menu, Settings, Save/Load, History, About, Help, Gallery and confirmation. Settings toggles were exercised (mute toggled twice and state restored). Gallery and modal confirmation completed the runtime smoke check with no exception. Screenshots in `docs/previews/gold/` are engine renders, not generated mockups. Verification used a separate save directory and the temporary harness is not shipped.
