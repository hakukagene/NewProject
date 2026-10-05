# Device appearance

The phone's **Тохиргоо → Утасны загвар** screen offers five complete appearances:

1. Clean Light — silver frame, coastal wallpaper, light surfaces, blue controls.
2. Midnight Glass — graphite frame, twilight wallpaper, translucent dark panels, violet controls.
3. Everyday Desktop — rounded rectangular frame, punch-hole camera, blue folded wallpaper and a clock widget.
4. Warm Personal — champagne frame, alpine wallpaper, cream/sage widgets and icons.
5. Moment Gold — gold frame, sunset wallpaper, charcoal surfaces and gold controls.

The selection applies immediately to the lock screen, home, app icons, Moment/chat, Music, Photos, Notes and desktop. Camera retains a dark capture surface. Open the desktop Settings icon for the same five choices. Desktop wallpaper fills the game canvas: there is no monitor bezel, stand or hardware frame. Browser/app windows remain usable with minimize, maximize, close and taskbar reopening.

Appearance is stored in `persistent.device_theme`, so loading an older story save, starting a new game or restarting does not reset the chosen design. An invalid saved theme safely falls back to Clean Light. Existing `moment_set_theme`/`moment_cycle_theme` callers route to the shared preference; legacy daylight/violet names map to Clean Light/Midnight Glass.

Assets: five generated WebP wallpapers, five transparent SVG phone frames, 40 themed SVG app icons and 12 SVG glyphs under `game/images/devices/`. Wallpapers were created with the built-in image generator, then encoded as WebP. Prompts: calm blue photographic coast; indigo alpine lake at twilight; sculptural blue folded satin; warm alpine lake/forest; charcoal mountain lake at gold sunset. All requested no interface, text, people or devices, with both landscape and central portrait framing. Icons and frame masks are native SVG to stay sharp and transparent.

Layout verification: Ren'Py 8.4.1 lint and in-engine screenshots of all five home/settings/chat/feed/music/notes and desktop/message/settings appearances, plus lock screen, expanded desktop, notes editor and free-phone mode. A separate two-process check confirmed restart persistence, invalid-theme fallback, required asset availability and unchanged story flags/relationships. Android camera capture still uses the existing native camera integration and was not exercised on an Android device. Story text, choices and relationship/block logic are unchanged.
