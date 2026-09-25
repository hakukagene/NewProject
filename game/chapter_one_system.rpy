# Save-backed story state. Existing Sara saves retain their original UI.
default stat_story_active = False
default stat_day_one_complete = False
default stat_location = "Өдөр 1"
default stat_relationships = {"khulan": 20, "anu": 35, "chingun": 40, "family": 20, "badral": 20, "dad": 40, "confidence": 20}
default stat_flags = {}
default stat_inspected = []
default stat_following_saruul = False
default stat_night_feed = False
default stat_notice = ""
default stat_post_likes = []
default stat_phone_tab = "feed"
default stat_story_contact = "khulan"
default stat_dm_replied = []

init python:
    CONTACTS = {
        "sara": {"name": "Болор", "handle": "bolor.bolor", "initial": "Б", "color": "#55c9bc", "status": "Америк · Businesswoman", "preview": "Өглөөний мэнд."},
        "khulan": {"name": "Хулан", "handle": "khulan.art", "initial": "Х", "color": "#ed95b3", "status": "Зураг зурж байна", "preview": "Хариад бичээрэй."},
        "anu": {"name": "Ану", "handle": "anu.cover", "initial": "А", "color": "#b4a0ea", "status": "Cover дуу", "preview": "Сайхан амраарай."},
        "saruul": {"name": "Саруул", "handle": "saruul.star", "initial": "С", "color": "#f3ad6b", "status": "Сургуулийн од", "preview": "Таныг дагалаа."},
        "chingun": {"name": "Чингүн", "handle": "chingun", "initial": "Ч", "color": "#87baf1", "status": "Идэвхтэй", "preview": "Анда, гэртээ харьсан уу?"},
    }
    POSTS = (
        ("khulan", "Өдрийн гэрэл. Шинэ дэвтэр. Шинэ танил.", "Шинэ зураг"),
        ("anu", "Зарим дууг ганцхан хүнд зориулж дуулдаг.", "Гитартай орой"),
        ("saruul", "Шинэ улирал эхэллээ.", "Campus day"),
        ("chingun", "Өнөөдөр гүйлтийн нормоо давуулчихлаа.", "Найзууд"),
    )
    INSPECTIONS = {
        "classroom": [
            ("class_window", "Цонх", "Нар Билгүүний ширээн дээр тусжээ. Хулан дэвтрээ яаран хаав."),
            ("class_students", "Ангийнхан", "Чингүн Хулангийн дэргэд сууна. Хулан зургийн дэвтэртэйгээ иржээ."),
            ("class_board", "Самбар", "Өнөөдрийн сэдэв — хүн өөрийн авьяасыг хэрхэн таних вэ?"),
        ],
        "khulan_room": [
            ("room_drawing", "Өлгөөтэй зургууд", "Хулан өдөр тутмын энгийн мөчүүдийг зурдаг ажээ."),
            ("room_awards", "Шагналууд", "Сурлага, урлагийн олон шагнал өрөөний нэг буланг дүүргэжээ."),
            ("piano_award", "Хамгийн дээд талын цом", "Төгөлдөр хуур — 1-р байр. Хулан зурахаас гадна хөгжимд авьяастай юм байна."),
        ],
    }

    def change(person, amount):
        state = dict(renpy.store.kh_relationships)
        state[person] = max(0, min(100, state.get(person, 20) + amount))
        renpy.store.kh_relationships = state

    def background(scene_id):
        path = "images/story/%s.webp" % scene_id
        if renpy.loadable(path):
            return Transform(path, xysize=(1920, 1080))
        night = scene_id in ("police_car", "bilguun_home", "bilguun_room", "dream")
        return Solid("#152132" if night else "#34424b")

    def start_story():
        renpy.store.kh_story_active = True
        renpy.store.moment_profile_name = "Билгүүн"
        renpy.store.moment_profile_handle = "bilguun"
        renpy.store.moment_profile_bio = "Оюутан · Эхний өдөр"
        renpy.store.moment_other_dm_messages = {}
        renpy.store.moment_contact_unread = {}
        renpy.store.moment_notifications = []
        renpy.store.moment_relationship_events = []
        renpy.store.sara_messages = []
        renpy.store.sara_unread_messages = 0
        renpy.store.phone_unlocked = True

    def receive(contact, text):
        messages = dict(renpy.store.moment_other_dm_messages)
        thread = list(messages.get(contact, []))
        thread.append({"sender": "contact", "text": text, "time": "Өнөөдөр"})
        messages[contact] = thread
        renpy.store.moment_other_dm_messages = messages

    def prepare_bolor():
        renpy.store.moment_relationship = 55
        renpy.store.sara_mood = "warm"
        renpy.store.sara_boundary_strikes = 0
        renpy.store.sara_blocked = False
        renpy.store.sara_cooldown_until = 0.0
        renpy.store.phone_chat_input = ""
        renpy.store.sara_messages = [
            {"sender": "sara", "text": "ogloonii mend. Egch n say l serlee. Hicheeliin ehnii odor her baiv", "time": "23:10"},
            {"sender": "player", "text": "Hi. Hicheel ntr yah ve. Onoodor manai angiin ohin nmg zurj baigaad chingvnd barigdaad angiar duuren ym bolloo", "time": "23:10"},
            {"sender": "sara", "text": "yeee. Emegtei huuhdiig yaj baigan. Chvs chi huurhun l haragdsan ym blgude", "time": "23:11"},
            {"sender": "player", "text": "Harin tiimee. Tgd bi argadaad bur geriinhentei n hool ntr ideed say irleeshd yooo XD", "time": "23:11"},
            {"sender": "sara", "text": "Aay chi neeree amjuuldag hun ym aa. Sayhan salsan ym baij XD", "time": "23:12"},
            {"sender": "player", "text": "Guee tanii bodoj baigaa shig bish XD", "time": "23:12"},
            {"sender": "sara", "text": "Zaa tiim bailgui dee gants duugee hund aldchihlaa gej ailaashd", "time": "23:13"},
            {"sender": "sara", "text": "Zaa jk shu XD", "time": "23:13"},
        ]
        receive("khulan", "Маргааш уулзъя. Хариад бичээрэй.")
        receive("chingun", "Анда, гэртээ харьсан уу?")

    def send_scripted_dm():
        contact = renpy.store.moment_active_contact
        message = renpy.store.phone_chat_input.strip()
        if not message:
            return
        messages = dict(renpy.store.moment_other_dm_messages)
        thread = list(messages.get(contact, []))
        thread.append({"sender": "player", "text": message, "time": phone_current_time()})
        if contact not in renpy.store.kh_dm_replied:
            responses = {
                "khulan": "Бичсэнийг чинь харлаа. Маргааш уулзъя.",
                "anu": "Хариулсанд баярлалаа. Сайхан амраарай.",
                "chingun": "За анда, маргааш уулзъя.",
                "saruul": "Мессежийг чинь харлаа. Одоо завгүй байна аа.",
            }
            thread.append({"sender": "contact", "text": responses.get(contact, "Seen"), "time": phone_current_time()})
            renpy.store.kh_dm_replied = renpy.store.kh_dm_replied + [contact]
        messages[contact] = thread
        renpy.store.moment_other_dm_messages = messages
        renpy.store.phone_chat_input = ""
        renpy.store.phone_chat_scroll_pending = True
        renpy.restart_interaction()

    def toggle_like(contact):
        liked = list(renpy.store.kh_post_likes)
        if contact in liked:
            liked.remove(contact)
        else:
            liked.append(contact)
        renpy.store.kh_post_likes = liked

screen scene_header():
    zorder 5
    frame:
        xpos 45
        ypos 35
        padding (24, 15)
        background Solid("#101725dc")
        text location size 24 color "#ffffff"

screen timed_choice(options, seconds):
    modal True
    default remaining = seconds
    timer 0.1 repeat True action If(remaining > 0.1, SetScreenVariable("remaining", remaining - 0.1), Return(len(options) - 1))
    frame:
        xalign 0.5
        yalign 0.65
        xsize 900
        padding (35, 30)
        background Solid("#101725f5")
        vbox:
            spacing 14
            text "Юу асуух вэ?" size 30
            bar value remaining range seconds xsize 830 ysize 8
            for i, option in enumerate(options):
                textbutton option action Return(i) xfill True

label inspect(room):
    $ stat_inspection_finished = False
    while not stat_inspection_finished:
        call screen inspection(room)
        if _return == "done":
            $ stat_inspection_finished = True
        else:
            $ stat_item = KH_INSPECTIONS[room][_return]
            if stat_item[0] not in stat_inspected:
                $ stat_inspected = stat_inspected + [stat_item[0]]
                if stat_item[0] == "piano_award":
                    $ stat_flags["knows_piano"] = True
            $ renpy.say(None, stat_item[2])
    return

screen inspection(room):
    modal True
    frame:
        xalign 0.5
        yalign 0.45
        xsize 1000
        padding (35, 35)
        background Solid("#152132ef")
        vbox:
            spacing 20
            text "Орчноо ажиглах" size 38
            for i, item in enumerate(KH_INSPECTIONS[room]):
                textbutton (item[1] + (" · Үзсэн" if item[0] in stat_inspected else "")) action Return(i)
            textbutton "Үргэлжлүүлэх":
                action Return("done")
                sensitive all(item[0] in stat_inspected for item in KH_INSPECTIONS[room])

screen computer():
    modal True
    add Solid("#0b1020")
    text "MOMENT / DESKTOP" xpos 95 ypos 65 size 36 color "#ffffff"
    text "Болор Болор" xpos 95 ypos 150 size 46 color "#9ae0db"
    text "Америк · Ганц бие · Businesswoman" xpos 95 ypos 220 size 24
    text "Өглөөний мэнд.\nЭндээс өөрөө чат бичиж болно." xpos 95 ypos 290 size 26
    text "AI хариулт интернет болон серверийн тохиргоо шаарддаг." xpos 95 ypos 405 xmaximum 680 size 22
    textbutton "Компьютероос босох":
        xpos 95
        ypos 560
        action Return()
        sensitive not sara_is_typing
    fixed:
        xpos 1050
        ypos 45
        xysize (624, 984)
        clipping True
        if phone_view == "chat":
            use phone_moment_chat
        else:
            use story_moment_page

screen phone_home():
    vbox:
        xpos 60
        ypos 220
        spacing 30
        text "Билгүүний утас" size 38 color "#ffffff"
        textbutton "Moment" action SetVariable("phone_view", "social") text_size 32
        textbutton "Music Player" action [Function(phone_music_open, "library"), SetVariable("phone_view", "music")] text_size 32
        textbutton "Утсаа тавих" action Return() text_size 25

screen moment_page():
    add Solid("#0c1019")
    use phone_status_bar(dark=True)
    text "moment" xpos 26 ypos 52 size 42 bold True color "#ffffff"
    textbutton "Утсаа тавих" xpos 407 ypos 58 text_size 20 action Return()
    hbox:
        xpos 20
        ypos 118
        spacing 14
        textbutton "Feed" action [SetVariable("phone_view", "social"), SetVariable("kh_phone_tab", "feed")] text_size 20
        textbutton "DM" action SetVariable("phone_view", "dm") text_size 20
        textbutton "Профайл" action SetVariable("phone_view", "profile") text_size 20
        textbutton "Music" action [Function(phone_music_open, "library"), SetVariable("phone_view", "music")] text_size 20
    viewport:
        xpos 24
        ypos 178
        xsize 576
        ysize 770
        mousewheel True
        draggable True
        vbox:
            spacing 22
            xsize 576
            if phone_view == "dm":
                for cid, person in CONTACTS.items():
                    textbutton (person["name"] + "  ·  " + person["handle"]):
                        action Function(moment_open_contact, cid)
                        text_size 25
                text "Болор — AI чат. Бусад дүр — зохиолын мессеж." size 19 color "#a9b4c5"
            elif phone_view in ("profile", "relationship"):
                text "Билгүүн / @bilguun" size 32
                text "52 дагагч     52 дагасан" size 24 color "#b4a0ea"
                for cid, title in [("khulan", "Хулан"), ("anu", "Ану"), ("chingun", "Чингүн"), ("badral", "Бадрал"), ("dad", "Аав")]:
                    text ("%s · %d / 100" % (title, kh_relationships[cid])) size 24
                text ("Болор · %d / 100" % moment_relationship) size 24
            elif kh_phone_tab == "story":
                $ person = CONTACTS[kh_story_contact]
                text (person["name"] + " · Story") size 30 color person["color"]
                $ post = next(item for item in POSTS if item[0] == kh_story_contact)
                text post[1] size 28 xmaximum 550
                textbutton "Мессеж бичих" action Function(moment_open_contact, kh_story_contact)
                textbutton "Буцах" action SetVariable("kh_phone_tab", "feed")
            else:
                if kh_notice:
                    text kh_notice size 23 color "#9ae0db"
                hbox:
                    spacing 10
                    for cid in ("khulan", "anu", "saruul", "chingun"):
                        textbutton CONTACTS[cid]["initial"]:
                            action [SetVariable("kh_story_contact", cid), SetVariable("kh_phone_tab", "story")]
                            text_size 30
                            xysize (120, 70)
                            background Solid(CONTACTS[cid]["color"])
                for cid, caption, title in KH_POSTS:
                    frame:
                        xsize 566
                        padding (20, 22)
                        background Solid("#1a2232")
                        vbox:
                            spacing 15
                            text CONTACTS[cid]["handle"] size 25 color CONTACTS[cid]["color"]
                            if renpy.loadable("images/story/post_%s.webp" % cid):
                                add ("images/story/post_%s.webp" % cid) xysize (526, 260)
                            else:
                                text title size 32
                            text caption size 24 xmaximum 520
                            hbox:
                                spacing 20
                                textbutton ("Таалагдсан" if cid in kh_post_likes else "Like") action Function(stat_toggle_like, cid) text_size 20
                                textbutton "DM" action Function(moment_open_contact, cid) text_size 20
                text "Reels · Бичлэг хараахан нэмэгдээгүй" size 22 color "#a9b4c5"

screen kh_day_summary():
    modal True
    add Solid("#0b1020")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        padding (50, 40)
        background Solid("#192337")
        vbox:
            spacing 20
            text "ӨДӨР 1 ДУУСЛАА" size 50 color "#ed95b3"
            text "Өдөр 2 — Үргэлжлэл" size 30
            text ("Хулан: %d · Ану: %d · Бадрал: %d" % (kh_relationships["khulan"], kh_relationships["anu"], kh_relationships["badral"])) size 26
            text ("Төгөлдөр хуурын шагналыг анзаарсан" if kh_flags.get("knows_piano") else "Шагналын нууц нээгдээгүй") size 24
            text "Үргэлжлэлийн зохиол хараахан нэмэгдээгүй." size 24
            textbutton "Дуусгах" action Return()
