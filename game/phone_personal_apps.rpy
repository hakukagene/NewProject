# Camera, in-game gallery, and notes for the phone. Gallery and notes are
# persistent across game saves; only the ten newest camera photos are kept.

default phone_camera_launch_pending = False
default phone_camera_pending_uri = ""
default phone_camera_message = ""
default phone_gallery_selected = -1
default phone_notes_page = "list"
default phone_note_selected = -1
default phone_note_draft_title = ""
default phone_note_draft_body = ""

init python:
    import datetime
    import os

    if persistent.phone_gallery_photos is None:
        persistent.phone_gallery_photos = []
    if persistent.phone_notes is None:
        persistent.phone_notes = []


    def phone_camera_open():
        renpy.store.phone_unlocked = True
        renpy.store.phone_unlock_pending = False
        renpy.store.phone_view = "camera"
        renpy.store.phone_camera_message = "Камерыг нээж байна…" if renpy.android else "Камерын зураг авах үйлдэл Android төхөөрөмж дээр ажиллана."
        renpy.store.phone_camera_launch_pending = bool(renpy.android)
        renpy.restart_interaction()


    def phone_camera_discard_pending():
        uri_text = renpy.store.phone_camera_pending_uri
        renpy.store.phone_camera_pending_uri = ""
        if not uri_text or not renpy.android:
            return
        try:
            from jnius import autoclass
            activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
            uri = autoclass("android.net.Uri").parse(uri_text)
            activity.getContentResolver().delete(uri, None, None)
        except Exception:
            pass


    def phone_camera_launch():
        store = renpy.store
        if not store.phone_camera_launch_pending or not renpy.android:
            return
        store.phone_camera_launch_pending = False
        phone_camera_discard_pending()
        try:
            from jnius import autoclass
            activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
            intent_type = autoclass("android.content.Intent")
            media = autoclass("android.provider.MediaStore$Images$Media")
            values = autoclass("android.content.ContentValues")()
            values.put("_display_name", "moment_%s.jpg" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            values.put("mime_type", "image/jpeg")
            uri = activity.getContentResolver().insert(media.EXTERNAL_CONTENT_URI, values)
            if uri is None:
                raise RuntimeError("Cannot create camera destination")
            store.phone_camera_pending_uri = uri.toString()
            intent = intent_type("android.media.action.IMAGE_CAPTURE")
            intent.putExtra("output", uri)
            intent.setClipData(autoclass("android.content.ClipData").newRawUri("moment_photo", uri))
            intent.addFlags(intent_type.FLAG_GRANT_READ_URI_PERMISSION | intent_type.FLAG_GRANT_WRITE_URI_PERMISSION)
            activity.startActivity(intent)
            store.phone_camera_message = "Зураг аваад баталгаажуулна уу."
        except Exception:
            phone_camera_discard_pending()
            store.phone_camera_message = "Камерыг нээж чадсангүй. Төхөөрөмжийн камерын аппыг шалгана уу."
        renpy.restart_interaction()


    def phone_camera_check():
        """Import the camera's output after its activity returns to Ren'Py."""
        uri_text = renpy.store.phone_camera_pending_uri
        if not uri_text or not renpy.android:
            return
        try:
            from jnius import autoclass
            activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
            uri = autoclass("android.net.Uri").parse(uri_text)
            descriptor = activity.getContentResolver().openFileDescriptor(uri, "r")
            if descriptor is None:
                return
            with os.fdopen(descriptor.detachFd(), "rb") as photo_file:
                data = photo_file.read(8 * 1024 * 1024 + 1)
            if len(data) > 8 * 1024 * 1024:
                renpy.store.phone_camera_message = "Зураг хэт том байна (8 MB-аас бага зураг авна уу)."
                phone_camera_discard_pending()
                renpy.restart_interaction()
                return
            # Empty destinations correspond to cancelled captures. Wait for a
            # complete JPEG rather than displaying a half-written image.
            if not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
                return
            photos = list(persistent.phone_gallery_photos or [])
            photos.insert(0, {"data": data, "time": datetime.datetime.now().strftime("%Y.%m.%d  %H:%M")})
            persistent.phone_gallery_photos = photos[:10]
            renpy.save_persistent()
            phone_camera_discard_pending()
            renpy.store.phone_camera_message = "Зураг хадгалагдлаа."
            renpy.store.phone_gallery_selected = 0
            renpy.store.phone_view = "gallery"
            renpy.restart_interaction()
        except Exception:
            # On some phones the camera has not finished writing yet.
            return


    def phone_gallery_items():
        return persistent.phone_gallery_photos or []


    def phone_gallery_delete(index):
        photos = list(phone_gallery_items())
        if 0 <= index < len(photos):
            del photos[index]
            persistent.phone_gallery_photos = photos
            renpy.save_persistent()
        renpy.store.phone_gallery_selected = -1
        renpy.restart_interaction()


    def phone_notes_open(index=-1):
        notes = persistent.phone_notes or []
        renpy.store.phone_note_selected = index if 0 <= index < len(notes) else -1
        note = notes[index] if 0 <= index < len(notes) else {}
        renpy.store.phone_note_draft_title = note.get("title", "")
        renpy.store.phone_note_draft_body = note.get("body", "")
        renpy.store.phone_notes_page = "editor"
        renpy.restart_interaction()


    def phone_notes_save(silent=False):
        store = renpy.store
        title = store.phone_note_draft_title.strip()[:80]
        body = store.phone_note_draft_body.strip()[:5000]
        if not title and not body:
            store.phone_notes_page = "list"
            return
        notes = list(persistent.phone_notes or [])
        index = store.phone_note_selected
        entry = {"title": title or "Шинэ тэмдэглэл", "body": body,
                 "time": datetime.datetime.now().strftime("%Y.%m.%d  %H:%M")}
        if 0 <= index < len(notes):
            notes[index] = entry
        else:
            notes.insert(0, entry)
        persistent.phone_notes = notes
        renpy.save_persistent()
        store.phone_note_selected = -1
        store.phone_notes_page = "list"
        if not silent:
            renpy.restart_interaction()


    def phone_notes_delete(index):
        notes = list(persistent.phone_notes or [])
        if 0 <= index < len(notes):
            del notes[index]
            persistent.phone_notes = notes
            renpy.save_persistent()
        renpy.store.phone_note_selected = -1
        renpy.store.phone_notes_page = "list"
        renpy.restart_interaction()


    def phone_note_preview(note):
        return phone_escape_chat_text((note.get("body", "") or "Хоосон тэмдэглэл").replace("\n", " ")[:100])


screen phone_camera_app():
    $ capture_action = [SetVariable("phone_camera_launch_pending", True), Function(phone_camera_launch)] if renpy.android else NullAction()
    add Solid("#0b1120")
    use phone_status_bar(dark=True)
    if phone_camera_launch_pending:
        timer 0.1 action Function(phone_camera_launch)
    elif phone_camera_pending_uri:
        timer 0.8 repeat True action Function(phone_camera_check)

    text "Камер" xpos 32 ypos 61 size 32 bold True color "#ffffff"
    textbutton "✕" xpos 544 ypos 58 text_size 28 text_color "#ffffff" background None action Function(phone_go_home)

    frame:
        xpos 28 ypos 155 xysize (568, 635)
        background Solid("#151e30")
        padding (26, 26)
        vbox:
            xalign 0.5 yalign 0.5 spacing 24
            text "◎" xalign 0.5 size 92 color "#62d8fa"
            text "[phone_camera_message]" xalign 0.5 xmaximum 460 text_align 0.5 size 22 color "#e2e8f0"
    button:
        xpos 249 ypos 819 xysize (126, 126)
        background Solid("#ffffff")
        hover_background Solid("#d7f6ff")
        padding (0, 0)
        action capture_action
        text "◎" xalign 0.5 yalign 0.5 size 72 color "#0b1120"
    textbutton "Зураг үзэх" xalign 0.5 ypos 945 text_size 19 text_color "#62d8fa" background None action [SetVariable("phone_gallery_selected", -1), SetVariable("phone_view", "gallery")]


screen phone_gallery_app():
    add Solid("#101a2b")
    use phone_status_bar(dark=True)
    $ photos = phone_gallery_items()
    textbutton "‹" xpos 22 ypos 56 text_size 36 text_color "#ffffff" background None action If(phone_gallery_selected >= 0, SetVariable("phone_gallery_selected", -1), Function(phone_go_home))
    text "Зураг" xpos 91 ypos 64 size 28 bold True color "#ffffff"
    text "[len(photos)] / 10" xpos 488 ypos 70 size 19 color "#94a3b8"
    add Solid("#334155") ypos 123 xysize (624, 1)

    if phone_gallery_selected >= 0 and phone_gallery_selected < len(photos):
        $ photo = photos[phone_gallery_selected]
        add im.Data(photo["data"], "camera.jpg") xpos 20 ypos 175 xysize (584, 638) fit "contain"
        text "[photo['time']]" xalign 0.5 ypos 843 size 21 color "#cbd5e1"
        textbutton "Устгах" xalign 0.5 ypos 898 text_size 21 text_color "#fb7185" background None action Function(phone_gallery_delete, phone_gallery_selected)
    elif photos:
        viewport:
            xpos 24 ypos 153 xsize 576 ysize 785
            mousewheel True draggable True
            vbox:
                spacing 12
                for row in range(0, len(photos), 3):
                    hbox:
                        spacing 12
                        for index in range(row, min(row + 3, len(photos))):
                            button:
                                xysize (184, 178)
                                padding (0, 0)
                                background Solid("#24364d")
                                action SetVariable("phone_gallery_selected", index)
                                add im.Data(photos[index]["data"], "camera.jpg") xalign 0.5 ypos 0 xysize (184, 145) fit "cover"
                                text "[photos[index]['time'][12:]]" xalign 0.5 ypos 149 size 16 color "#cbd5e1"
    else:
        text "Зураг хараахан алга" xalign 0.5 ypos 432 size 26 color "#cbd5e1"
        text "Камераар авсан сүүлийн 10 зураг энд хадгалагдана." xalign 0.5 ypos 477 xmaximum 510 text_align 0.5 size 20 color "#94a3b8"
    textbutton "Камер нээх" xalign 0.5 ypos 939 text_size 20 text_color "#62d8fa" background None action Function(phone_camera_open)


screen phone_notes_app():
    add Solid("#f7f6f1")
    use phone_status_bar()
    if phone_notes_page == "editor":
        textbutton "‹ Тэмдэглэл" xpos 28 ypos 59 text_size 22 text_color "#9b6e12" background None action Function(phone_notes_save)
        textbutton "Болсон" xpos 509 ypos 59 text_size 21 text_color "#9b6e12" background None action Function(phone_notes_save)
        add Solid("#e7e4da") ypos 122 xysize (624, 1)
        frame:
            xpos 30 ypos 152 xysize (564, 70)
            background Solid("#ffffff") padding (14, 9)
            input value VariableInputValue("phone_note_draft_title") length 80 color "#202838" size 26 xsize 520
        text "Агуулга" xpos 40 ypos 248 size 19 color "#9a9a90"
        frame:
            xpos 30 ypos 287 xysize (564, 592)
            background Solid("#ffffff") padding (17, 17)
            input value VariableInputValue("phone_note_draft_body") length 5000 multiline True copypaste True color "#263346" size 22 xysize (518, 552)
        if phone_note_selected >= 0:
            textbutton "Тэмдэглэл устгах" xalign 0.5 ypos 920 text_size 19 text_color "#d95c58" background None action Function(phone_notes_delete, phone_note_selected)
    else:
        text "Тэмдэглэл" xpos 35 ypos 72 size 35 bold True color "#1b2636"
        $ notes = persistent.phone_notes or []
        text "[len(notes)] тэмдэглэл" xpos 39 ypos 130 size 19 color "#868c91"
        add Solid("#e1ded5") ypos 170 xysize (624, 1)
        if notes:
            viewport:
                xpos 28 ypos 195 xsize 568 ysize 690
                mousewheel True draggable True
                vbox:
                    spacing 10
                    for index, note in enumerate(notes):
                        button:
                            xysize (568, 117)
                            padding (18, 10)
                            background Solid("#ffffff")
                            hover_background Solid("#fff3ce")
                            action Function(phone_notes_open, index)
                            vbox:
                                spacing 5
                                text "[phone_escape_chat_text(note['title'])]" size 22 bold True color "#222d3c" xmaximum 520
                                text "[phone_note_preview(note)]" size 18 color "#7d8790" xmaximum 510
                                text "[note['time']]" size 15 color "#aa9c7b"
        else:
            text "Одоогоор тэмдэглэл алга" xalign 0.5 ypos 433 size 24 color "#747e8a"
            text "+ товчоор эхний тэмдэглэлээ бичээрэй." xalign 0.5 ypos 477 size 19 color "#a0a7ad"
        button:
            xpos 510 ypos 884 xysize (78, 78)
            background Solid("#f5bc4b") hover_background Solid("#ffd278")
            padding (0, 0) action Function(phone_notes_open)
            text "+" xalign 0.5 yalign 0.5 size 42 color "#ffffff"
