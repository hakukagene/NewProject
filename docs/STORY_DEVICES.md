# Story phone and desktop

The cafeteria message opens Anu's conversation inside the phone. At night,
Bilguun opens Moment in a desktop browser, then checks his phone's home screen.
Both devices share the same conversation history, relationship state, likes,
music library/playback, camera photographs and persistent notes.

## Desktop

- Desktop shortcuts and the taskbar open Moment, Music, Notes and Photos.
- The window controls minimize, maximize/restore, or close the current window.
  A taskbar button reopens it. Escape minimizes the window first; Escape again
  leaves the computer. The explicit leave button is always available.
- Moment has Home, Messages and Profile pages. The three-column message view
  uses the existing contact, AI and relationship logic without embedding a phone.
- Messages wrap; the draft expands to a bounded height, then scrolls. Send with the
  button or Ctrl+Enter. Enter adds a line break. Drafts are kept per contact.
- Notes save when switching apps, changing notes, closing or leaving. The phone
  sees these same notes. Photos shows the same ten-photo phone library.

## Phone

- A clock, latest message card and six app icons replace the story's text menu.
- Moment has a feed, story cards, inbox and profile with a bottom tab bar.
- Swipe upward from the bottom edge to return home (no visible swipe line).
  On the home screen, choose “Утсаа тавих” to continue the chapter.
- Camera, Photos, Notes and Music route to their existing apps in story mode.
  The Android camera requirement is unchanged; desktop does not emulate a camera.
- While typing, the phone's secondary composer icons collapse to give the draft
  more width. Camera and gallery shortcuts open the corresponding phone apps.

The browser address is an in-game `moment.local` address, not an external website.
Bolor still requires the existing configured chatbot service. The other contacts
use the story's scripted responses. AI requests continue if the window is closed;
closing a device does not cancel or silently replace a reply.

## Implementation and validation

Device screens and desktop helpers: `game/story_devices.rpy`.
Story entry points: `game/chapter_one.rpy` and `game/story_system.rpy`.
Contact switching and drafts: `game/moment_app.rpy`.
Personal app routing: `game/phone_ui.rpy`.

An unused alternate screen in `chapter_one_system.rpy` referenced a missing
`kh_moment_page`, preventing all screens from preparing at startup. That reference
now uses the canonical `story_moment_page`; the alternate story code is retained.

Run `python -m unittest discover -s tests -v` and Ren'Py Check Script/Lint.
Desktop and phone screens were also rendered in Ren'Py 8.4.1 for visual checking.
Target-device Android camera permissions and the live AI service are separate
integration checks and were not exercised by the UI verification.

Screenshots: [Desktop](previews/desktop.png), [phone home](previews/phone-home.png),
[long phone draft](previews/phone-chat.png).
