# customersurvey.py

my [original customer survey](https://github.com/erroronline1/customersurvey) for wamp was all fun and games until the battery of the cheap windows tablet started to inflate. now, replacing a cheap windows-tablet turned out to be nearly impossible in 2023 from a german public service point of view.

this is now my first somewhat successful compiled android app usind python3, [kivy](https://kivy.org/) and [kivyMD](https://kivymd.readthedocs.io) that makes it possible to use a cheap android tablet instead.

## app-features

* multi language survey
* multi language admin
* rtf report including analysis
* csv export
* configurable timeouts, presets, colour palette
* partially configurable borders

exports will be stored within the documents-folder. on pc as well as on android device.

supported languages dependent on used fonts. cyrillic works, arabic does not by default.

![screenshot](https://raw.githubusercontent.com/erroronline1/customersurvey.py/master/images/screenshot.png)

## usage

* once compiled using buildozer install the apk on the device
* on initial start the database will be initialized. you will be asked to provide a password. do not forget this, for you will have to provide it to access any admin options, including data export. if you loose the password only removing and reinstalling the app will make it usable again. all data will be lost.
* you can set the timeout, colour palette and default languages for your audience
* you can set up border spacings to some amount to match possible frames for the device

most settings take effect only after restarting the app. 

## code-features

* handling of environment, desktop by default, android by conditional platform
* language easily extendable within own module
* questions can be modified within the language module. the database doesn't care. provided questions will be implemented within the report. requires a new compiling process though

sorry for the excitement, but i'm just freaking glad it works w/o needing to learn java. i'm not totally sure about every buildozer.spec setting, but it works now.

tested on Samsung Galaxy S9 @ Android10, Samsumg Galaxy S10 @ Android12

## resources

1. Mariyas video on [Convert Python to Android with WINDOWS & LINUX + Fix Common Bugs](https://www.youtube.com/watch?v=VsTaM057rdc)
2. explanations on [private storage handling](https://github.com/Android-for-Python/Android-for-Python-Users#private-storage)
3. rescue on [cross-api storage handling](https://github.com/Android-for-Python/androidstorage4kivy)

