image pBorder = "images/phoneUI/phoneborder.png"
image pWallpaper = "images/phoneUI/wallpaper.png"
image pBattery = "images/phoneUI/battery.png"
image lockScreenGray = AlphaMask(Solid("#050816a6", xysize=(800, 1199)), "images/phoneUI/wallpaper.png")
image homeScreenBlackOverlay = AlphaMask(Solid("#00000099", xysize=(800, 1199)), "images/phoneUI/wallpaper.png")
image pBorderOverlay = AlphaMask("images/phoneUI/phoneborder.png", "images/phoneUI/wallpaper.png", invert=True)

# The source icon PNGs contain several hundred pixels of transparent padding.
# Crop that padding before scaling so the visible artwork is centred in its
# quick-action button. The source sizes below also compensate for the lock
# screen's non-uniform fit transform, so the final on-screen icons keep the
# proportions seen on a real phone lock screen.
image pLightOff = Transform(
    AlphaMask(
        Solid("#ffffff", xysize=(102, 202)),
        Crop((255, 212, 102, 202), "images/phoneUI/lightOff.png")
    ),
    xysize=(18, 34)
)

image pLightOn = Transform(
    AlphaMask(
        Solid("#fff4a8", xysize=(102, 263)),
        Crop((255, 151, 102, 263), "images/phoneUI/lightOn.png")
    ),
    xysize=(18, 44)
)

image pCameraIcon = Transform(
    AlphaMask(
        Solid("#ffffff", xysize=(346, 266)),
        Crop((317, 357, 346, 266), "images/phoneUI/CameraIcon.png")
    ),
    xysize=(40, 22)
)

image pQuickActionBackground = "images/phoneUI/quick_action_background.svg"
image pSwipeLine = "images/phoneUI/swipe_line.svg"
image pNotificationGlass = "images/phoneUI/notification_glass.svg"
image pMomentNotificationIcon = "images/phoneUI/moment_notification_icon.svg"

# The phone content is scaled more vertically than horizontally. These icon
# sources are intentionally 84x66 so they become square on the final screen.
image pHomeMomentIcon = AlphaMask(Solid("#7c3aed", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeChatIcon = AlphaMask(Solid("#10b981", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeCameraIcon = AlphaMask(Solid("#0ea5e9", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeGalleryIcon = AlphaMask(Solid("#ec4899", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeNotesIcon = AlphaMask(Solid("#f59e0b", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeSettingsIcon = AlphaMask(Solid("#64748b", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeMusicIcon = AlphaMask(Solid("#1b77c4", xysize=(84, 66)), "images/phoneUI/home_app_icon_mask.svg")
image pHomeStoryIcon = Transform("pHomeNotesIcon", xysize=(68, 53))





#moment application icons
image pHome = Transform("images/phoneUI/Momenticon/home.png", xysize=((50, 40)))
image pDM = Transform("images/phoneUI/Momenticon/dm.png", xysize=((50, 40)))
image pComment = Transform("images/phoneUI/Momenticon/comment.png", xysize=((50, 40)))
image pProfile = Transform("images/phoneUI/Momenticon/profile.png", xysize=((50, 40)))
image pSend = Transform("images/phoneUI/Momenticon/send.png", xysize=((50, 40)))
image pPicture = Transform("images/phoneUI/Momenticon/picture.png", xysize=((50, 40)))
image pSticker = Transform("images/phoneUI/Momenticon/sticker.png", xysize=((50, 40)))
image pAdd = Transform("images/phoneUI/Momenticon/add.png", xysize=((50, 40)))
