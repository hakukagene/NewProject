# Corner phone notification

A permanent phone button appears at the top right during story dialogue and choices. Clicking it opens the phone home screen in a separate Ren'Py context. Closing the phone resumes the same interaction. The button is hidden while the full phone or story computer is open and in the main menu.

Scripted incoming messages display a gold/brown notification beside the icon for eight visible seconds. Clicking the notification opens that contact's conversation. The icon shows the unread-message count. Messages remain in the existing conversation history after the toast disappears. Long notification text can scroll within the card.

The opening Anu message no longer forces the full phone to open. Its original text and the cover listen/skip choices are preserved. Other scripted phone/computer scenes continue as before.

Validation: Ren'Py 8.4.1 lint, rendered actual notification, opening the real phone at home and at Anu's thread in a nested context and returning, unread clearing assertion. The temporary test timer and harness were removed. Physical touch devices and live AI arrivals were not tested; the new toast is hooked to scripted story_receive messages.
