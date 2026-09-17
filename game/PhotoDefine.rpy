image pBorder = "images/phoneUI/phoneborder.png"
image pWallpaper = "images/phoneUI/wallpaper.png"
image pBattery = "images/phoneUI/battery.png"
image lockScreenGray = AlphaMask(Solid("#050816a6", xysize=(800, 1199)), "images/phoneUI/wallpaper.png")
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
