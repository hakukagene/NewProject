# A local music player for the in-game phone. Put additional audio files under
# game/audio/music/; Ren'Py includes them in desktop and mobile builds.

default phone_music_view = "library"
default phone_music_return_view = "library"
default phone_music_list_kind = ""
default phone_music_list_key = ""
default phone_music_query = ""
default phone_music_new_name = ""
default phone_music_current = ""
default phone_music_order = []
default phone_music_favorites = []
default phone_music_recent = []
default phone_music_play_counts = {}
default phone_music_custom_playlists = {"My Playlist": []}
default phone_music_dialog = ""
default phone_music_selected = ""
default phone_music_shuffle = False

image pMusicBackground = "images/phoneUI/music_player_bg.svg"
image pMusicCover = "images/phoneUI/music_player_cover.svg"
image pMusicRoundButton = "images/phoneUI/music_round_button.svg"

init -1 python:
    renpy.music.register_channel("phone_music", mixer="music", loop=False)


init python:
    import functools
    import os
    import random

    PHONE_MUSIC_DEMOS = {
        "audio/music/blue_hour.ogg": {
            "title": "Blue Hour",
            "artist": "Moment Originals",
            "album": "On the Road",
            "duration": 24,
        },
        "audio/music/night_train.ogg": {
            "title": "Night Train",
            "artist": "Moment Originals",
            "album": "On the Road",
            "duration": 24,
        },
    }
    PHONE_MUSIC_TYPES = (".ogg", ".opus", ".mp3", ".flac", ".wav")
    PHONE_MUSIC_AUTO = (
        ("favorites", "Favorite", "♡"),
        ("recent_add", "Recent add", "◷"),
        ("recent_play", "Recent play", "↻"),
        ("most_play", "Most play", "♪"),
    )


    def phone_music_safe(value):
        """Keep file names from being interpreted as Ren'Py text markup."""
        return str(value).replace("[", "[[").replace("{", "{{")


    @functools.lru_cache(maxsize=1)
    def phone_music_catalog():
        tracks = []
        for path in sorted(renpy.list_files()):
            if not path.startswith("audio/music/") or not path.lower().endswith(PHONE_MUSIC_TYPES):
                continue
            file_name = path.rsplit("/", 1)[-1]
            folder = path.rsplit("/", 2)[-2]
            metadata = PHONE_MUSIC_DEMOS.get(path, {})
            tracks.append({
                "path": path,
                "title": metadata.get("title") or os.path.splitext(file_name)[0].replace("_", " "),
                "artist": metadata.get("artist") or "Local artist",
                "album": metadata.get("album") or "My Music",
                "folder": folder if folder != "music" else "Music",
                "duration": metadata.get("duration"),
            })
        return tracks


    def phone_music_tracks(kind="", key=""):
        tracks = phone_music_catalog()
        if kind == "album":
            return [track for track in tracks if track["album"] == key]
        if kind == "artist":
            return [track for track in tracks if track["artist"] == key]
        if kind == "folder":
            return [track for track in tracks if track["folder"] == key]
        if kind == "playlist":
            paths = []
            if key == "favorites":
                paths = renpy.store.phone_music_favorites
            elif key == "recent_add":
                paths = [track["path"] for track in reversed(tracks)]
            elif key == "recent_play":
                paths = renpy.store.phone_music_recent
            elif key == "most_play":
                counts = renpy.store.phone_music_play_counts
                paths = sorted(counts, key=lambda path: -counts[path])
                paths = [path for path in paths if counts[path] > 0]
            else:
                paths = renpy.store.phone_music_custom_playlists.get(key, [])
            lookup = {track["path"]: track for track in tracks}
            return [lookup[path] for path in paths if path in lookup]
        return tracks


    def phone_music_groups(kind):
        counts = {}
        for track in phone_music_catalog():
            label = track[kind]
            counts[label] = counts.get(label, 0) + 1
        return sorted(counts.items(), key=lambda item: item[0].casefold())


    def phone_music_playlists():
        entries = []
        for key, title, icon in PHONE_MUSIC_AUTO:
            entries.append((key, title, icon, len(phone_music_tracks("playlist", key))))
        for name in renpy.store.phone_music_custom_playlists:
            entries.append((name, name, "♫", len(phone_music_tracks("playlist", name))))
        return entries


    def phone_music_navigation():
        return (
            ("♫", "TRACKS", len(phone_music_catalog()), "tracks"),
            ("◎", "ALBUMS", len(phone_music_groups("album")), "albums"),
            ("♙", "ARTISTS", len(phone_music_groups("artist")), "artists"),
            ("▱", "FOLDER", len(phone_music_groups("folder")), "folder"),
        )


    def phone_music_open(view):
        renpy.store.phone_music_view = view
        renpy.store.phone_music_dialog = ""


    def phone_music_open_group(kind, key):
        renpy.store.phone_music_list_kind = kind
        renpy.store.phone_music_list_key = key
        phone_music_open("list")


    def phone_music_back():
        store = renpy.store
        if store.phone_music_dialog:
            store.phone_music_dialog = ""
        elif store.phone_music_view == "player":
            store.phone_music_view = store.phone_music_return_view
        elif store.phone_music_view == "list" and store.phone_music_list_kind in ("album", "artist", "folder"):
            store.phone_music_view = {"album": "albums", "artist": "artists", "folder": "folder"}[store.phone_music_list_kind]
        else:
            store.phone_music_view = "library"


    def phone_music_track(path):
        for track in phone_music_catalog():
            if track["path"] == path:
                return track
        return None


    def phone_music_record_play(path):
        store = renpy.store
        store.phone_music_recent = [path] + [item for item in store.phone_music_recent if item != path][:29]
        counts = dict(store.phone_music_play_counts)
        counts[path] = counts.get(path, 0) + 1
        store.phone_music_play_counts = counts


    def phone_music_play(path, order=None):
        available = {track["path"] for track in phone_music_catalog()}
        if path not in available:
            return
        order = [item for item in (order or []) if item in available]
        order = list(dict.fromkeys(order))
        if path not in order:
            order.insert(0, path)
        start = order.index(path)
        renpy.store.phone_music_order = order
        renpy.store.phone_music_current = path
        phone_music_record_play(path)
        renpy.music.play(order[start:] + order[:start], channel="phone_music",
                        loop=False, fadeout=0.2, fadein=0.2)


    def phone_music_sync():
        """Follow Ren'Py's real playback position as a queued song changes."""
        path = renpy.music.get_playing(channel="phone_music")
        if path and path != renpy.store.phone_music_current and phone_music_track(path):
            renpy.store.phone_music_current = path
            phone_music_record_play(path)


    def phone_music_selected_track():
        store = renpy.store
        path = renpy.music.get_playing(channel="phone_music") or store.phone_music_current
        tracks = phone_music_catalog()
        return phone_music_track(path) or (tracks[0] if tracks else None)


    def phone_music_toggle():
        playing = renpy.music.get_playing(channel="phone_music")
        if playing:
            renpy.music.set_pause(not renpy.music.get_pause(channel="phone_music"),
                                channel="phone_music")
            return
        track = phone_music_selected_track()
        if track:
            phone_music_play(track["path"], renpy.store.phone_music_order or [t["path"] for t in phone_music_catalog()])


    def phone_music_is_active():
        return (bool(renpy.music.get_playing(channel="phone_music"))
                and not renpy.music.get_pause(channel="phone_music"))


    def phone_music_skip(direction):
        track = phone_music_selected_track()
        if not track:
            return
        available = {item["path"] for item in phone_music_catalog()}
        order = [path for path in renpy.store.phone_music_order if path in available]
        if not order:
            order = [item["path"] for item in phone_music_catalog()]
        current = renpy.music.get_playing(channel="phone_music") or track["path"]
        index = order.index(current) if current in order else 0
        if direction < 0:
            position = renpy.music.get_pos(channel="phone_music") or 0
            if position > 3:
                phone_music_play(current, order)
                return
        phone_music_play(order[(index + direction) % len(order)], order)


    def phone_music_shuffle_all():
        order = [track["path"] for track in phone_music_catalog()]
        if not order:
            return
        random.shuffle(order)
        renpy.store.phone_music_shuffle = True
        phone_music_play(order[0], order)


    def phone_music_toggle_favorite(path):
        items = list(renpy.store.phone_music_favorites)
        if path in items:
            items.remove(path)
        else:
            items.append(path)
        renpy.store.phone_music_favorites = items


    def phone_music_create_playlist():
        store = renpy.store
        name = store.phone_music_new_name.strip()[:28]
        if not name:
            number = 1
            while "Playlist %s" % number in store.phone_music_custom_playlists:
                number += 1
            name = "Playlist %s" % number
        if name in store.phone_music_custom_playlists or name in [entry[0] for entry in PHONE_MUSIC_AUTO]:
            renpy.notify("Ийм нэртэй playlist байна.")
            return
        items = dict(store.phone_music_custom_playlists)
        items[name] = []
        store.phone_music_custom_playlists = items
        store.phone_music_new_name = ""
        store.phone_music_dialog = ""
        phone_music_open_group("playlist", name)


    def phone_music_add_to_playlist(path, name):
        items = dict(renpy.store.phone_music_custom_playlists)
        if name in items and phone_music_track(path):
            songs = list(items[name])
            if path not in songs:
                songs.append(path)
            items[name] = songs
            renpy.store.phone_music_custom_playlists = items
        renpy.store.phone_music_dialog = ""


    def phone_music_remove_from_playlist(path, name):
        items = dict(renpy.store.phone_music_custom_playlists)
        if name in items:
            items[name] = [item for item in items[name] if item != path]
            renpy.store.phone_music_custom_playlists = items
        renpy.store.phone_music_dialog = ""


    def phone_music_open_player():
        if renpy.store.phone_music_view != "player":
            renpy.store.phone_music_return_view = renpy.store.phone_music_view
        phone_music_open("player")


    def phone_music_open_track_menu(path):
        renpy.store.phone_music_selected = path
        renpy.store.phone_music_dialog = "track"


    def phone_music_time(seconds):
        seconds = max(0, int(seconds or 0))
        return "%d:%02d" % (seconds // 60, seconds % 60)


    def phone_music_progress():
        track = phone_music_selected_track()
        if not track or not track["duration"]:
            return 0.0
        position = renpy.music.get_pos(channel="phone_music") or 0
        return max(0.0, min(1.0, position / float(track["duration"])))


screen phone_music_app():
    add "pMusicBackground"
    add Solid("#072e5c44")
    use phone_status_bar(dark=True)
    timer 0.5 repeat True action Function(phone_music_sync)

    if phone_music_view == "library":
        use phone_music_library
    elif phone_music_view == "player":
        use phone_music_player
    elif phone_music_view == "search":
        use phone_music_search
    else:
        use phone_music_browser

    if phone_music_view != "player":
        use phone_music_mini_player
    if phone_music_dialog:
        use phone_music_popup


screen phone_music_header(title="Music Player"):

    fixed:
        ypos 42
        xysize (624, 78)

        textbutton ("☰" if phone_music_view == "library" else "‹"):
            xpos 25
            yalign 0.5
            text_size 32
            text_color "#ffffff"
            background None

            action If(
                phone_music_view == "library",
                SetVariable("phone_music_dialog", "menu"),
                Function(phone_music_back)
            )

        text "[phone_music_safe(title)]":
            xpos 96
            yalign 0.5
            size 26
            color "#ffffff"
            xmaximum 425

        if phone_music_view != "search":
            button:
                xpos 548
                ypos 12
                xysize (58, 54)
                padding (0, 0)
                background None
                hover_background Solid("#ffffff1a")
                action Function(phone_music_open, "search")

                add "images/phoneUI/music_search.svg" xalign 0.5 yalign 0.5

    add Solid("#ffffff32") ypos 119 xysize (624, 1)


screen phone_music_library():
    use phone_music_header

    hbox:
        xpos 16
        ypos 135
        spacing 0
        for icon, label, count, view in phone_music_navigation():
            button:
                xysize (148, 102)
                padding (0, 0)
                background Solid("#ffffff09")
                hover_background Solid("#ffffff20")
                action Function(phone_music_open, view)
                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 3
                    fixed:
                        xalign 0.5
                        xysize (60, 42)
                        text "[icon]" xalign 0.5 yalign 0.5 size 34 color "#ffcf43"
                    text "[label]" xalign 0.5 size 18 color "#ffffff"
                    text "([count])" xalign 0.5 size 15 color "#d2e7ff"

    add Solid("#ffffff45") ypos 244 xysize (624, 1)
    text "Playlists ([len(phone_music_playlists())])":
        xpos 32
        ypos 258
        size 20
        color "#ffffff"
    button:
        xpos 514
        ypos 250
        xysize (72, 48)
        padding (0, 0)
        background None
        hover_background Solid("#ffffff1b")
        action SetVariable("phone_music_dialog", "new")
        text "+" xalign 0.5 yalign 0.5 size 33 color "#ffffff"

    viewport:
        xpos 22
        ypos 302
        xsize 580
        ysize 575
        mousewheel True
        draggable True
        scrollbars None
        vbox:
            spacing 4
            for key, title, icon, count in phone_music_playlists():
                button:
                    xysize (578, 90)
                    padding (0, 0)
                    background Solid("#ffffff13")
                    hover_background Solid("#ffffff28")
                    action Function(phone_music_open_group, "playlist", key)
                    fixed:
                        xysize (578, 90)
                        fixed:
                            xpos 12
                            yalign 0.5
                            xysize (76, 58)
                            add Solid("#2367a6aa")
                            text "[icon]" xalign 0.5 yalign 0.5 size 32 color "#ffffff"
                        vbox:
                            xpos 106
                            yalign 0.5
                            spacing 4
                            text "[phone_music_safe(title)]" size 21 color "#ffffff" xmaximum 400
                            text "[count] songs" size 16 color "#c4dcfa"
                        text "›" xpos 536 yalign 0.5 size 32 color "#ffffff"

    textbutton "⇄":
        xpos 500
        ypos 800
        xysize (88, 64)
        text_size 38
        text_color "#ffffff"
        text_hover_color "#ffffff"
        text_xalign 0.5
        text_yalign 0.5
        background "pMusicRoundButton"
        hover_background "pMusicRoundButton"
        action Function(phone_music_shuffle_all)


screen phone_music_browser():
    $ view = phone_music_view
    $ groups = phone_music_groups("album" if view == "albums" else "artist" if view == "artists" else "folder")
    $ title = phone_music_list_key if view == "list" else {"tracks": "Tracks", "albums": "Albums", "artists": "Artists", "folder": "Folder"}.get(view, "Music")
    use phone_music_header(title)

    if view == "list" or view == "tracks":
        $ songs = phone_music_tracks(phone_music_list_kind, phone_music_list_key) if view == "list" else phone_music_catalog()
        text "[len(songs)] songs":
            xpos 30
            ypos 138
            size 18
            color "#c4dcfa"
        if view == "list" and phone_music_list_kind == "playlist" and songs:
            textbutton "▶  Play all":
                xpos 458
                ypos 126
                text_size 18
                text_color "#ffcf43"
                background None
                action Function(phone_music_play, songs[0]["path"], [track["path"] for track in songs])
        viewport:
            xpos 22
            ypos 181
            xsize 580
            ysize 690
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 5
                if not songs:
                    text "Энд одоохондоо дуу алга." size 21 color "#d4e9ff" xalign 0.5 ypos 84
                for track in songs:
                    use phone_music_track_row(track, [item["path"] for item in songs])
    else:
        text "[len(groups)] collections":
            xpos 30
            ypos 139
            size 18
            color "#c4dcfa"
        viewport:
            xpos 22
            ypos 180
            xsize 580
            ysize 690
            mousewheel True
            draggable True
            scrollbars None
            vbox:
                spacing 6
                for label, count in groups:
                    button:
                        xysize (578, 92)
                        background Solid("#ffffff16")
                        hover_background Solid("#ffffff2b")
                        action Function(phone_music_open_group, "album" if view == "albums" else "artist" if view == "artists" else "folder", label)
                        fixed:
                            xysize (555, 80)
                            add Solid("#1e65a3aa") xpos 8 ypos 11 xysize (78, 58)
                            text ("◎" if view == "albums" else "♙" if view == "artists" else "▱") xpos 23 ypos 18 size 32 color "#ffcf43"
                            text "[phone_music_safe(label)]" xpos 98 ypos 11 size 22 color "#ffffff" xmaximum 410
                            text "[count] songs" xpos 98 ypos 46 size 16 color "#c4dcfa"


screen phone_music_track_row(track, order):
    $ path = track["path"]
    fixed:
        xysize (578, 84)
        button:
            xysize (578, 84)
            padding (0, 0)
            background Solid("#ffffff15")
            hover_background Solid("#ffffff2a")
            action Function(phone_music_play, path, order)
            fixed:
                xysize (578, 84)
                add "pMusicCover" xpos 6 ypos 12 xysize (80, 60)
                text "[phone_music_safe(track['title'])]" xpos 100 ypos 13 size 20 color "#ffffff" xmaximum 340
                text "[phone_music_safe(track['artist'])]" xpos 100 ypos 49 size 16 color "#c6dffb" xmaximum 324
        textbutton ("♥" if path in phone_music_favorites else "♡"):
            xpos 444
            ypos 21
            text_size 26
            text_color "#ffcf43"
            background None
            action Function(phone_music_toggle_favorite, path)
        textbutton "⋮":
            xpos 524
            ypos 22
            text_size 27
            text_color "#ffffff"
            background None
            action Function(phone_music_open_track_menu, path)


screen phone_music_search():
    use phone_music_header("Search")
    add Solid("#ffffff22") xpos 26 ypos 143 xysize (572, 60)
    input:
        xpos 42
        ypos 156
        xsize 526
        size 22
        color "#ffffff"
        length 40
        value VariableInputValue("phone_music_query")
    $ query = phone_music_query.strip().casefold()
    $ songs = [track for track in phone_music_catalog() if query in (track["title"] + " " + track["artist"] + " " + track["album"]).casefold()]
    viewport:
        xpos 22
        ypos 229
        xsize 580
        ysize 645
        mousewheel True
        draggable True
        scrollbars None
        vbox:
            spacing 5
            if not songs:
                text "Илэрц олдсонгүй." size 20 color "#d4e9ff" xalign 0.5 ypos 70
            for track in songs:
                use phone_music_track_row(track, [item["path"] for item in songs])


screen phone_music_mini_player():
    $ current = phone_music_selected_track()
    add Solid("#062855f2") ypos 884 xysize (624, 100)
    add Solid("#ffffff35") ypos 883 xysize (624, 1)
    if current:
        button:
            xpos 8
            ypos 892
            xysize (410, 86)
            padding (0, 0)
            background None
            hover_background Solid("#ffffff15")
            action Function(phone_music_open_player)
            fixed:
                xysize (410, 86)
                add "pMusicCover" xpos 6 ypos 10 xysize (88, 66)
                text "[phone_music_safe(current['title'])]" xpos 108 ypos 16 size 20 color "#ffffff" xmaximum 275
                text "[phone_music_safe(current['artist'])]" xpos 108 ypos 50 size 16 color "#c4dcfa" xmaximum 265
        textbutton ("Ⅱ" if phone_music_is_active() else "▶"):
            xpos 428
            ypos 907
            text_size 30
            text_color "#ffffff"
            background None
            action Function(phone_music_toggle)
        textbutton "▶▌":
            xpos 510
            ypos 907
            text_size 24
            text_color "#ffffff"
            background None
            action Function(phone_music_skip, 1)
    else:
        text "game/audio/music/ хавтас руу дуу нэмээрэй.":
            xpos 25
            ypos 922
            size 18
            color "#ffffff"


screen phone_music_player():
    $ current = phone_music_selected_track()
    use phone_music_header("Now Playing")
    if current:
        add "pMusicCover" xpos 96 ypos 198 xysize (432, 320)
        text "[phone_music_safe(current['title'])]":
            xalign 0.5
            ypos 600
            size 31
            color "#ffffff"
        text "[phone_music_safe(current['artist'])]":
            xalign 0.5
            ypos 649
            size 20
            color "#cde4ff"
        textbutton ("♥" if current["path"] in phone_music_favorites else "♡"):
            xpos 538
            ypos 599
            text_size 30
            text_color "#ffcf43"
            background None
            action Function(phone_music_toggle_favorite, current["path"])
        add Solid("#ffffff52") xpos 60 ypos 710 xysize (504, 7)
        add Solid("#ffcf43") xpos 60 ypos 710 xysize (max(2, int(504 * phone_music_progress())), 7)
        text "[phone_music_time(renpy.music.get_pos(channel='phone_music'))]":
            xpos 60
            ypos 727
            size 17
            color "#ffffff"
        $ duration_text = phone_music_time(current["duration"]) if current["duration"] else "--:--"
        text "[duration_text]":
            xpos 564
            xanchor 1.0
            ypos 727
            size 17
            color "#ffffff"
        textbutton "▌◀":
            xpos 134
            ypos 777
            text_size 28
            text_color "#ffffff"
            background None
            action Function(phone_music_skip, -1)
        textbutton ("Ⅱ" if phone_music_is_active() else "▶"):
            xpos 268
            ypos 770
            xysize (88, 64)
            text_xalign 0.5
            text_yalign 0.5
            text_size 31
            text_color "#ffffff"
            background "pMusicRoundButton"
            hover_background "pMusicRoundButton"
            action Function(phone_music_toggle)
        textbutton "▶▌":
            xpos 437
            ypos 777
            text_size 28
            text_color "#ffffff"
            background None
            action Function(phone_music_skip, 1)
        textbutton "⇄ Shuffle":
            xalign 0.5
            ypos 870
            text_size 19
            text_color "#ffcf43"
            background None
            action Function(phone_music_shuffle_all)
    else:
        text "Дуу олдсонгүй. game/audio/music/ хавтас руу дуу нэмээрэй.":
            xalign 0.5
            ypos 390
            xmaximum 520
            text_align 0.5
            size 21
            color "#ffffff"


screen phone_music_popup():
    button:
        xysize (624, 984)
        padding (0, 0)
        background Solid("#020e27b8")
        hover_background Solid("#020e27b8")
        action SetVariable("phone_music_dialog", "")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 504
        background Solid("#153f73")
        padding (24, 22)
        vbox:
            xfill True
            spacing 12
            if phone_music_dialog == "menu":
                text "Music Player" size 27 bold True color "#ffffff" xalign 0.5
                add Solid("#ffffff30") xysize (456, 1)
                textbutton "⌂   Утасны нүүр":
                    xsize 456
                    text_size 21
                    text_color "#ffffff"
                    background Solid("#ffffff10")
                    padding (16, 12)
                    action Function(phone_go_home)
                textbutton "♫   Tracks":
                    xsize 456
                    text_size 21
                    text_color "#ffffff"
                    background Solid("#ffffff10")
                    padding (16, 12)
                    action Function(phone_music_open, "tracks")
                textbutton "▤   Playlists":
                    xsize 456
                    text_size 21
                    text_color "#ffffff"
                    background Solid("#ffffff10")
                    padding (16, 12)
                    action Function(phone_music_open, "library")
            elif phone_music_dialog == "new":
                text "Шинэ playlist" size 27 color "#ffffff"
                frame:
                    xysize (456, 60)
                    background Solid("#ffffff27")
                    padding (12, 8)
                    input value VariableInputValue("phone_music_new_name") length 28 color "#ffffff" size 22
                textbutton "Үүсгэх" text_size 22 text_color "#ffcf43" action Function(phone_music_create_playlist)
            elif phone_music_dialog == "track":
                $ selected = phone_music_track(phone_music_selected)
                $ selected_title = phone_music_safe(selected["title"]) if selected else "Дуу"
                text "[selected_title]" size 25 color "#ffffff"
                if phone_music_list_kind == "playlist" and phone_music_list_key in phone_music_custom_playlists and phone_music_selected in phone_music_custom_playlists[phone_music_list_key]:
                    textbutton "Playlist-аас хасах" text_size 20 text_color "#ffffff" action Function(phone_music_remove_from_playlist, phone_music_selected, phone_music_list_key)
                viewport:
                    xysize (456, min(310, max(55, len(phone_music_custom_playlists) * 58)))
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 4
                        for name in phone_music_custom_playlists:
                            textbutton "[phone_music_safe(name)]-д нэмэх" text_size 20 text_color "#ffffff" action Function(phone_music_add_to_playlist, phone_music_selected, name)
            textbutton "Хаах":
                text_size 20
                text_color "#aacff6"
                action SetVariable("phone_music_dialog", "")
