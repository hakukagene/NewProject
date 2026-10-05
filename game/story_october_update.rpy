# Added scenes from the October 2 screenplay.
define story_aggressor = Character("Залуу")
define story_students = Character("Оюутнууд")

label story_october_night:
    $ story_location = "Өдөр 2 · Билгүүний өрөө · Шөнө"
    scene expression story_background("bilguun_room") with dissolve
    $ story_set_test_actors(('bilguun',))
    show screen story_scene_header
    "Билгүүн компьютерынхоо ард сууж, Болортой чатлана."
    $ story_append_bolor_night()
    $ story_desktop_open("moment")
    $ story_desktop_page = "messages"
    $ moment_active_contact = "sara"
    $ phone_view = "chat"
    hide screen story_scene_header
    call screen story_computer
    show screen story_scene_header
    "Энэ зуур Анугаас мессеж ирэв."
    if not story_flags.get("anu_farewell_received"):
        $ story_receive("anu", "Chmg nz ohintoi bolsniig harsaan. Bayr hurgey. Chinii omnoos jargaltai bn. Yu ch bolson bi chinii toloo buuj ogohgui gesen ch ene udaad uneheer buuj ogohiig huslee. Hamtdaa ongrooson buh dursamjuud, hamt hiij baisan duu bolgoniigoo hezee ch bitgii martaarai. Ndad zoriulj hiij bsan duugaa nz ohindoo zoriulj duulj ogoorei. Chmg jargaltai baigaa gej naidiy. Hairtai shuu. Biye bodooroi. Chinii huurhun gogo n.")
        $ story_flags["anu_farewell_received"] = True
    $ story_desktop_open("moment")
    $ story_desktop_page = "messages"
    $ moment_open_contact("anu")
    hide screen story_scene_header
    call screen story_computer
    show screen story_scene_header
    "Билгүүн орондоо ороод утсаараа Moment нээв. Ану «Гогогоос нь сүүлийн удаа» гэсэн тайлбартай cover нийтэлжээ. Хулан цэцэг тэвэрсэн story оруулсан байлаа."
    $ story_flags["oct02_night_feed"] = True
    $ phone_unlocked = True
    $ phone_view = "social"
    $ story_phone_tab = "feed"
    hide screen story_scene_header
    call screen phone_ui
    show screen story_scene_header
    "Билгүүн утсаа тавиад унтлаа."
    return

label story_october_day_three:
    $ story_day = 3
    $ story_location = "Өдөр 3 · Сургуулийн коридор · Өглөө"
    scene expression story_background("corridor") with dissolve
    $ story_set_test_actors(('bilguun',))
    show screen story_scene_header
    "Сургуулийн коридорт зарлалын самбарын урд хүүхдүүд шавхыг харсан Билгүүн дөхөн очлоо."
    story_students "Энэ одоо ямар бүдүүлэг юм бэ? Атаманаа ч хатдаа, Юу болсон юм бол?"
    "Зарлалын самбарт Чингүний зургийг хоёр нүдэн дээр нь X зурж хаджээ. Доор нь «Арын талбайд арван цагт» гэсэн бичиг, нэг лого байв. Хажууд нь «Пэдофил хүмүүс бидний эргэн тойронд» гэсэн сонины нийтлэл харагдана."
    "Билгүүн зургийг урж аваад цагаа харвал арав өнгөрчээ. Арын талбайд хүн байсангүй. Чингүний цүнх газар хэвтэнэ. Машины зогсоолоос дуу гарахад Билгүүн тийш гүйв."
    $ story_location = "Өдөр 3 · Сургуулийн машины зогсоол"
    scene expression story_background("school_parking") with dissolve
    $ story_set_test_actors(('bilguun', 'chingun', 'older_students'))
    show screen story_scene_header
    "Хэдэн залуу газарт унасан Чингүнийг тойрон зодож байлаа."
    bilguun "Болиоч!"
    story_aggressor "Чи Чингүнтэй цуг зугтаад байсан залуу байна тэ. Чи бас энэнтэй хамаатай юу?"
    menu:
        "Би Чингүний найз нь байна. Та нар яахаараа найз поольддог билээ.":
            $ story_flags["oct02_choice_1"] = "А"
            bilguun "Би Чингүний найз нь байна. Та нар яахаараа найз поольддог билээ."
        "Тийм байна. Ямар асуудал байна? Хүн шиг хэлээрээ олж болдоггүй мал уу?":
            $ story_flags["oct02_choice_1"] = "Б"
            bilguun "Тийм байна. Ямар асуудал байна? Хүн шиг хэлээрээ олж болдоггүй мал уу?"
        "Найзыгаа аваад явчих уу? Асуудал тарьчихгүйхэн шиг":
            $ story_flags["oct02_choice_1"] = "В"
            bilguun "Найзыгаа аваад явчих уу? Асуудал тарьчихгүйхэн шиг"
        "Чам шиг гөлөг хөөж байсныг мэдсэн бол зугтах ч гүй байсан юм.":
            $ story_flags["oct02_choice_1"] = "Г"
            bilguun "Чам шиг гөлөг хөөж байсныг мэдсэн бол зугтах ч гүй байсан юм."
    story_aggressor "Бас нэг том ам шалдан гуя. Аваад ир энийг."
    "Гурван залуу Билгүүн рүү гүйж ирэхэд тэр гараа зангидав."
    call story_parking_fight
    "Билгүүн хоёр залууг унагасан ч олны хүчийг дийлсэнгүй. Түүнийг Чингүний хажууд газарт шидэв."
    story_aggressor "За Чингүнээ ахынхаа юмыг хэзээ өгөх гэж байна? Би чамайг үржүүлээд ирээ гэсэн үү үрээд ир гэсэн үү?"
    chingun "Түй май алаад аваарай."
    menu:
        "Чингүнээ чи юуг нь авчихсан юм бэ?":
            $ story_flags["oct02_choice_2"] = "А"
            bilguun "Чингүнээ чи юуг нь авчихсан юм бэ?"
        "Чингүнээ энэ хүн юу яриад байна?":
            $ story_flags["oct02_choice_2"] = "Б"
            bilguun "Чингүнээ энэ хүн юу яриад байна?"
        "Хөөе ах гуйа манай найз таны юуг чинь авчихаад сүржигнээд байгаа юм?":
            $ story_flags["oct02_choice_2"] = "В"
            bilguun "Хөөе ах гуйа манай найз таны юуг чинь авчихаад сүржигнээд байгаа юм?"
        "Чимээгүй өнгөрөх":
            $ story_flags["oct02_choice_2"] = "Г"
            "Чимээгүй өнгөрөх"
    if story_flags.get("oct02_choice_2") == "А":
        chingun "Би энэ хүний юуг ч аваагүй ээ."
    if story_flags.get("oct02_choice_2") == "Б":
        chingun "Чи энд яах гэж ирсэн бэ? Мань нь өөрөө зохицуулчихна шдээ."
    if story_flags.get("oct02_choice_2") == "В":
        chingun "Ахаа. Манай найз ямар ч хамаагүй ээ. Надтай л ярь"
    if story_flags.get("oct02_choice_2") == "Г":
        chingun "Билгүүнээ намайг хэлэхээр босоод гүйгээрэй."
    "Залуу Чингүний гэдэс рүү өшиглөв."
    story_aggressor "За. Чи мэддэггүй юм уу? Танай энэ Чингүнээ найз чинь…"
    "Энэ үед араас нь Саруулын машин орж ирэн сигналдах ба дотроос нь Саруул утсаараа бичлэг хийн гарч ирнэ."
    $ story_set_test_actors(("bilguun", "chingun", "saruul"))
    saruul "За манайхаан, энийг хар даа. Өөрөөсөө нас бага хүүхдүүдийг олноороо нийлж ийм болтол нь зодож, дээрэлхэж, дээрэмдэж байна. Цагдаа дуудаарай, манайхан!"
    "Саруул шууд дамжуулалт хийж байгаа мэт жүжиглэнэ."
    story_aggressor "Чи ямар их артай лалар вэ?"
    "гэж Чингүнд хэлэх ба Саруул уруу хэдэн залуучууд дөхнө."
    saruul "Заа одоо намайг барьж авж зодох нь."
    "гэх үед Саруулын араас том биетэй хамгаалагч нар нь гүйж ирэх ба нөгөө залуучууд зугтацгаана."
    story_aggressor "Би гэрийг чинь мэднэ ээ Чингүнээ"
    "Саруул Билгүүн Чингүн хоёр дээр очино."
    saruul "Зүгээр үү та хоёр. Би машинаа тавих гэж байгаад хараад ирлээ."
    chingun "Аан би зүгээр ээ. Таны улаан фэн чинь шүү."
    menu:
        "Чи ирээгүй бол хэцүүдэх л байлаа.":
            $ story_flags["oct02_choice_3"] = "А"
            bilguun "Чи ирээгүй бол хэцүүдэх л байлаа."
        "Баярлалаа. Бид хоёр зүгээр дээ.":
            $ story_flags["oct02_choice_3"] = "Б"
            bilguun "Баярлалаа. Бид хоёр зүгээр дээ."
        "Чингүнээс болж би дандаа ингэж юманд өртөх юм аа тэ Чингүнээ.":
            $ story_flags["oct02_choice_3"] = "В"
            bilguun "Чингүнээс болж би дандаа ингэж юманд өртөх юм аа тэ Чингүнээ."
        "Инээх":
            $ story_flags["oct02_choice_3"] = "Г"
            "Инээх"
    if story_flags.get("oct02_choice_3") == "Г":
        "Саруул хариу инээв."
    saruul "Би та хоёрыг эмнэлэгт хүргээд өгье. Аймар болчихсон байна шдээ."
    menu:
        "Хэрэггүй ээ. Бид хоёр зүгээр ээ.":
            $ story_flags["oct02_choice_4"] = "А"
            bilguun "Хэрэггүй ээ. Бид хоёр зүгээр ээ."
        "Эвгүй шүүдээ. Бид хоёр өөрсдөө бологчихно оо.":
            $ story_flags["oct02_choice_4"] = "Б"
            bilguun "Эвгүй шүүдээ. Бид хоёр өөрсдөө бологчихно оо."
        "Үсрээд л толгой хагарсан биз. Ямар үхсэн биш яах юм бэ.":
            $ story_flags["oct02_choice_4"] = "В"
            bilguun "Үсрээд л толгой хагарсан биз. Ямар үхсэн биш яах юм бэ."
        "Заа эр хүмүүсд ийм юм байх. Сүржигнэх хэрэггүй ээ":
            $ story_flags["oct02_choice_4"] = "Г"
            bilguun "Заа эр хүмүүсд ийм юм байх. Сүржигнэх хэрэггүй ээ"
    chingun "Ёо ёо ёо. Анда аймар өвдөөд байна аа. Анай эмнэлэг хүргээд өгөөрэй яаг үхлээ."
    "Ингээд Билгүүн Чингүн Саруул гурав эмнэлэгрүү явлаа."
    $ story_flags["saruul_rescued_friends"] = True
    $ story_location = "Өдөр 3 · Саруулын машин · Өдөр"
    scene expression story_background("saruul_car") with dissolve
    $ story_set_test_actors(('bilguun', 'chingun', 'saruul'))
    show screen story_scene_header
    saruul "Та хоёрыг яалаа гэж ингэж аймар зодох уу?"
    menu:
        "Харин яагаад юм бол оо? Чингүнээ!":
            $ story_flags["oct02_choice_5"] = "А"
            bilguun "Харин яагаад юм бол оо? Чингүнээ!"
        "Мэдэх юм алга. Нэг юм нэхээд л байсан шд.":
            $ story_flags["oct02_choice_5"] = "Б"
            bilguun "Мэдэх юм алга. Нэг юм нэхээд л байсан шд."
        "Чингүнээ л сайн мэдэж байгаа байх даа? хэр хүнд асуудал юм бэ дээ?":
            $ story_flags["oct02_choice_5"] = "В"
            bilguun "Чингүнээ л сайн мэдэж байгаа байх даа? хэр хүнд асуудал юм бэ дээ?"
        "Харин манай найз асуудал тарьсан юм шиг л байна. IDOLдоо худлаа хэлэхгүй юм байгаа…":
            $ story_flags["oct02_choice_5"] = "Г"
            bilguun "Харин манай найз асуудал тарьсан юм шиг л байна. IDOLдоо худлаа хэлэхгүй юм байгаа биз дээ Чингүнээ?"
    if story_flags.get("oct02_choice_5") == "А":
        chingun "Мань нь чамд дараа хэлье. Сүртэй асуудал бишээ."
    if story_flags.get("oct02_choice_5") == "Б":
        chingun "Мань юм хумыг нь аваагүй ээ. Хүн андуураад байгаа юм."
    if story_flags.get("oct02_choice_5") == "В":
        chingun "Асуудал нтр биш ээ анда. Намайг андуураад байгаа юм аа."
    if story_flags.get("oct02_choice_5") == "Г":
        chingun "Хэзээ би чамд худлаа хэлж байсан юм. Хэхэ манай найз жоохон ууртай хүн л дээ зөвөөр ойлгоорой анай."
    saruul "Хүний санаа зовоогоод хаячих юм Билгүүнээ."
    "Саруулын Билгүүнээ гэж хэлэхийг сонссон Билгүүн Чингүн Саруул гурав хэсэг шоконд оров."
    chingun "Та хоёр бие биенээ таньдаг юм уу?"
    menu:
        "Юу гэж дээ. Чамайг л Билгүүнээ гэж дуудаж байхыг сонссон байлгүй дээ.":
            $ story_flags["oct02_choice_6"] = "А"
            bilguun "Юу гэж дээ. Чамайг л Билгүүнээ гэж дуудаж байхыг сонссон байлгүй дээ."
        "Ийм том од хүнийг юу гэж таньдаг байхав дээ.":
            $ story_flags["oct02_choice_6"] = "Б"
            bilguun "Ийм том од хүнийг юу гэж таньдаг байхав дээ."
        "Харин тийн та намайг яаж таньдаг юм?":
            $ story_flags["oct02_choice_6"] = "В"
            bilguun "Харин тийн та намайг яаж таньдаг юм?"
        "Чимээгүй өнгөрөх":
            $ story_flags["oct02_choice_6"] = "Г"
            "Чимээгүй өнгөрөх"
    if story_flags.get("oct02_choice_6") == "А":
        saruul "Аанхан. Чи тэгсэн шд"
    if story_flags.get("oct02_choice_6") == "Б":
        saruul "Чи Билгүүнээ л гээд байсан шүү дээ"
    if story_flags.get("oct02_choice_6") == "В":
        saruul "Өө… юу… тийн… Сургуулийнхан бүгд л чамайг мэднэ шд. Билгүүн гээд"
    if story_flags.get("oct02_choice_6") == "Г":
        saruul "…"
    if story_flags.get("oct02_choice_6") in ("А", "Б"):
        chingun "Би Билгүүнээ гэсэн юм уу? Сонин юм даа."
    elif story_flags.get("oct02_choice_6") == "В":
        chingun "Юу вэ? Билгүүнээг сургуулиараа байтугай би ч арай гэж таньдаг шдээ."
    else:
        "Чингүн Билгүүн рүү ширтэв."
    "Эмнэлэгийн үүдэнд ирэв. Тэр 3 эмнэлэг орно."
    $ story_location = "Өдөр 3 · Эмнэлгийн гадаа · Орой"
    scene expression story_background("hospital_exterior") with dissolve
    $ story_set_test_actors(('bilguun', 'saruul'))
    show screen story_scene_header
    "Гадаа орой болсон байв. Саруул машиндаа суун нөгөө хоёрыг хүлээж байх ба Билгүүнээ эмнэлэгээс гараад ирэв. Билгүүн Саруул дээр очив."
    saruul "Заа цаадах чинь хэр байна?"
    bilguun "Гайгүй гэнэ ээ. Дусал нтр хийлгээд байгаад л байна."
    menu:
        "Тусалсанд баярласан шүү. Чамайг хараад авралын сахиусан тэнгэр л гэж бодлоо":
            $ story_flags["oct02_choice_7"] = "А"
            bilguun "Тусалсанд баярласан шүү. Чамайг хараад авралын сахиусан тэнгэр л гэж бодлоо"
        "Чи сая машинд өөрөө гэн алдах гэж байна шд.":
            $ story_flags["oct02_choice_7"] = "Б"
            bilguun "Чи сая машинд өөрөө гэн алдах гэж байна шд."
        "Өдөржин бид хоёрыг хүлээсэн юм уу? Яахнав дээ бүтэн өдрийн ажлаа алдчихлаа шд.":
            $ story_flags["oct02_choice_7"] = "В"
            bilguun "Өдөржин бид хоёрыг хүлээсэн юм уу? Яахнав дээ бүтэн өдрийн ажлаа алдчихлаа шд."
        "Аая сэтгэлтэй эмэгтэй юм аа. Ийм болоод л хүмүүс чамд дуртай байдаг байх аа.":
            $ story_flags["oct02_choice_7"] = "Г"
            bilguun "Аая сэтгэлтэй эмэгтэй юм аа. Ийм болоод л хүмүүс чамд дуртай байдаг байх аа."
    if story_flags.get("oct02_choice_7") == "А":
        saruul "Паа сүртэй шд. Би тэнд явж байсан нь аз. Үгүй бол чи эмнэлэгт үхсэн ирэх байсан байлгүй. Энд суугаад жоохон хоол идчих"
    if story_flags.get("oct02_choice_7") == "Б":
        saruul "Харин тийм ээ. Худлаа ярьж чаддаггүй хүн чинь ямар хэцүү юм бэ? Ийшээ суугаад жоохон юм идчих"
    if story_flags.get("oct02_choice_7") == "В":
        saruul "Зүгээр ээ. Та хоёрт санаа зовоод байх юм байна шд. Суугаад жоохон юм идчих."
    if story_flags.get("oct02_choice_7") == "Г":
        saruul "Чиний бодож байгаагаас илүү сэтгэлтэй шүү. Май хоол ид."
    "Билгүүн Саруулын машины урд тал суугаад хоол иднэ. Энэ зуур алсаас нэг хүн тэр хоёрыг ажиглаж байх ба зургыг нь аваад явчихав."
    $ story_flags["saruul_photo_taken"] = True
    "Саруулын утсанд VCALL орж ирнэ. Хоёр дүү нь залгаж байна."
    story_sibling "Анай, та хэзээ ирэх юм бэ?"
    saruul "Анай нь энд ажилтай л байна. Яасан бэ хоёроо. Зүгээр үү."
    story_sibling "Анай намайг битгий загинаарай. Би эннээс нь татчихсан чинь ус гараад зогсохгүй байна."
    saruul "Юу? Алив анай нь хариядаа. Яанаа анай нь наадхыг чинь мэдэхгүй шдээ."
    saruul "Чи ус янзалж чадах уу?"
    menu:
        "Чаднаа.":
            $ story_flags["oct02_choice_8"] = "А"
            bilguun "Чаднаа."
        "Алив хурдан хөдлөөрэй. Би тогтоогоод өгье.":
            $ story_flags["oct02_choice_8"] = "Б"
            bilguun "Алив хурдан хөдлөөрэй. Би тогтоогоод өгье."
        "Би чадахгүй шдээ. Мэддэг хүн дуудаарай.":
            $ story_flags["oct02_choice_8"] = "В"
            bilguun "Би чадахгүй шдээ. Мэддэг хүн дуудаарай."
        "Би ийм юм өмнө нь харж ч байгаагүй шдээ":
            $ story_flags["oct02_choice_8"] = "Г"
            bilguun "Би ийм юм өмнө нь харж ч байгаагүй шдээ"
    if story_flags.get("oct02_choice_8") == "В":
        saruul "Эр хүн байж. За очоод учир нь олдох байлгүй."
    elif story_flags.get("oct02_choice_8") == "Г":
        saruul "Заа одоо чиний туслах ээлж."
    "Саруул машинаа хөдөлгөж, Билгүүнийг гэр лүүгээ авч явлаа."
    $ story_location = "Өдөр 3 · Саруулын гэр · Шөнө"
    scene expression story_background("saruul_home") with dissolve
    $ story_set_test_actors(('bilguun', 'saruul'))
    show screen story_scene_header
    "Билгүүн угаалтуурын доор ноцолдоно. Саруул хажуу талд нь ширээнийхээ ард тооцоо бодож сууна. Дүү нар нь унтсан байлаа. Билгүүн засаад дууссав."
    $ story_flags["saruul_sink_fixed"] = True
    saruul "За ашгүй дээ. Эр хүний гар хаяа яахын аргагүй дутдаг шүү."
    menu:
        "Нээх сүртэй юм болоогүй байж ээ. Одоо зүгээр болсон.":
            $ story_flags["oct02_choice_9"] = "А"
            bilguun "Нээх сүртэй юм болоогүй байж ээ. Одоо зүгээр болсон."
        "Танай хоёр сахилгагүй өнөөдөр нилээн уйдсан бололтой.":
            $ story_flags["oct02_choice_9"] = "Б"
            bilguun "Танай хоёр сахилгагүй өнөөдөр нилээн уйдсан бололтой."
        "Хэрэг гарвал хэлж байхгүй юу даа. Элдэв хүн дуудаж байхаар.":
            $ story_flags["oct02_choice_9"] = "В"
            bilguun "Хэрэг гарвал хэлж байхгүй юу даа. Элдэв хүн дуудаж байхаар."
        "Гэрт үү? Чамд уу?":
            $ story_flags["oct02_choice_9"] = "Г"
            bilguun "Гэрт үү? Чамд уу?"
    if story_flags.get("oct02_choice_9") == "А":
        saruul "Заа баярлалаа. Энийг солиод өмсчих. Цамц чинь бүр норчихож."
    if story_flags.get("oct02_choice_9") == "Б":
        saruul "Өдөржин би байхгүй дураараа л дуригсан биз."
    if story_flags.get("oct02_choice_9") == "В":
        saruul "Угаасаа намайг мэдэж байгаа нь чи л юм чинь чамайг л дуудна. Муриад байв тэгээд. Энийг солиод өмсчих май"
    if story_flags.get("oct02_choice_9") == "Г":
        saruul "Ёооё, Өдөөрэй. Май энийг солиод өмсчих. Яаж нойтон юмтай явхав дээ."
    bilguun "Энэ юу юм?"
    saruul "Аавд ээж авч байсан мак л байна. Шинэ юм байна. Юм бодохгүй солиод өмсчихгүй юу."
    "Билгүүн норсон цамцаа сольж өмсөнө. Саруул түүнийг сэм харснаа ичингүйрэн өөр тийш харав. Билгүүн хувцсаа солиод Саруул дээр очлоо."
    menu:
        "Өнөөдөр болсон зүйл бид гурвын нууц шүү":
            $ story_flags["oct02_choice_10"] = "А"
            bilguun "Өнөөдөр болсон зүйл бид гурвын нууц шүү"
        "Хүний нууцаар харах муухай даа.":
            $ story_flags["oct02_choice_10"] = "Б"
            bilguun "Хүний нууцаар харах муухай даа."
        "Чи надад ингэж байгаад дуралчихвий лээ.":
            $ story_flags["oct02_choice_10"] = "В"
            bilguun "Чи надад ингэж байгаад дуралчихвий лээ."
        "Чи хурдан нөхөртэй болохгүй бол болохгүй нь дээ тэ.":
            $ story_flags["oct02_choice_10"] = "Г"
            bilguun "Чи хурдан нөхөртэй болохгүй бол болохгүй нь дээ тэ."
    if story_flags.get("oct02_choice_10") == "А":
        saruul "Хоёулаа дундаа ямар их нууцтай болж байна аа. за 1 1 шүү. Нээрээ бичлэгэнд санаа зоволтгүй шүү. Би устагчихсан."
    if story_flags.get("oct02_choice_10") == "Б":
        saruul "Нууцаар ч гэх шиг. Чиний юуг хархав дээ... Гоё биетэй л юм байна."
    if story_flags.get("oct02_choice_10") == "В":
        saruul "Чиний юунд дурлахав дээ. Гоё биенд чинь уу? Санаа зоволтгүй ээ миний дүү."
    if story_flags.get("oct02_choice_10") == "Г":
        saruul "Яасан их юманд санаа зовж байх юм? Эсвэл чи надтай суух юм уу? хаха"
    if story_flags.get("oct02_choice_10") == "А":
        bilguun "ок. За би явлаа."
    if story_flags.get("oct02_choice_10") == "Б":
        bilguun "Харах юм байгаа л биз дээ. хаха За би явлаа."
    if story_flags.get("oct02_choice_10") == "В":
        bilguun "Заа тэгвэл санаа зовохоо болилоо шүү. Би явлаа."
    if story_flags.get("oct02_choice_10") == "Г":
        bilguun "Хаха инээдтэй байлаа. За би явлаа."
    if story_flags.get("oct02_choice_10") == "А":
        $ story_flags["saruul_recording_deleted_known"] = True
    "Билгүүн юм хумаа аваад Саруулын гэрээс гарлаа. Билгүүн Хулангийнхруу нэг хараад гэрийн зүг алхана."
    $ story_location = "Өдөр 3 · Билгүүний гэрийн үүд · Шөнө"
    scene expression story_background("bilguun_home") with dissolve
    $ story_set_test_actors(('bilguun', 'khulan'))
    show screen story_scene_header
    "Билгүүн алхасаар гэрийнхээ гадаа иртэл гэрийнх нь үүдэнд Хулан зогсож байна. Билгүүн гайхсаар дөхөж очино."
    $ story_flags["khulan_waiting_at_home"] = True
    $ story_flags["oct02_scenes_complete"] = True
    return

# Save-backed choices and QTE results; no wall-clock state survives a reload.
default story_fight_score = 0
default story_fight_round = 0

init python:
    def story_append_bolor_night():
        if story_flags.get("bolor_second_night_seeded"):
            return
        story_flags["bolor_second_night_seeded"] = True
        # Scripted setup must respect the relationship boundary established by play.
        if sara_blocked or sara_boundary_strikes >= 4 or sara_cooldown_until > __import__("time").time():
            return
        lines = (
            ("player", "Bi sain2 Taniar yu bn"),
            ("sara", "Ania n baij l baina. Ajildaa yvh geed l."),
            ("player", "Mni nuguu ochigdor taniltssan ohin nz zaluutai bsn bn lee shd. Gehdee unuudur bas aygu sonin huntei taniltssan."),
            ("sara", "Oo ydg muu ohin be. Minii huurhun duugeer togloh gej bsn bnshd. Za bas ymr huntei ve"),
            ("player", "Bi tanid daraa helnee"),
            ("sara", "♥"),
        )
        renpy.store.sara_messages = list(sara_messages) + [
            {"sender": sender, "text": text, "time": "23:15"}
            for sender, text in lines
        ]
        renpy.store.phone_chat_scroll_pending = True

    def story_current_posts():
        if story_flags.get("oct02_night_feed"):
            return (
                ("anu", "Гогогоос нь сүүлийн удаа", "Анугийн сүүлчийн cover"),
                ("khulan", "Цэцэг тэвэрсэн Хулангийн story.", "Оройн цэцэг"),
            ) + tuple(post for post in STORY_POSTS if post[0] not in ("anu", "khulan"))
        return STORY_POSTS

label story_parking_fight:
    $ story_fight_score = 0
    $ story_fight_round = 0
    "Дайсны цохилтын чиглэлийг ажиглаад эсрэг тийш бултаарай. A / D, зүүн / баруун сум, доорх товч эсвэл swipe ашиглана."
    while story_fight_round < 6:
        call screen story_fight_prompt(STORY_DODGE_ATTACKS[story_fight_round], story_fight_round, story_fight_score)
        if _return:
            $ story_fight_score += 1
        call screen story_dodge_feedback(_return, STORY_DODGE_ATTACKS[story_fight_round])
        $ story_fight_round += 1
    $ story_flags["parking_fight_score"] = story_fight_score
    $ story_flags["parking_fight_complete"] = True
    "Та [story_fight_score] / 6 хөдөлгөөнийг цагт нь хийлээ."
    return
