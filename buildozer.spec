[app]
title = PrankApp
package.name = prankapp
package.domain = com.yourname.prank
source.dir = .
version = 1.0
source.include_exts = py,png,jpg,mp3,gif
requirements = python3, kivy, plyer
android.permissions = INTERNET, VIBRATE, SYSTEM_ALERT_WINDOW, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.service = True
android.presplash_color = #000000
android.add_asset_dirs = assets

[buildozer]
log_level = 2
warn_on_root = 0
