# customersurvey.py

my [original customer survey](https://github.com/erroronline1/customersurvey) for wamp was all fun and games until the battery of the cheap windows tablet started to inflate. now, replacing a cheap windows-tablet turned out to be nearly impossible in 2023 from a german public service point of view.

this is now my first somewhat successful compiled android app using python3, [kivy](https://kivy.org/) and [kivyMD](https://kivymd.readthedocs.io) that makes it possible to use a cheap android tablet instead.

## download a working apk
<a href="https://drive.google.com/file/d/15s_p4JuECNqlcLo_-L4UMzBEHjGEeXj9/view?usp=share_link" target="_blank">>>> link to google drive <<<</a>

## app-features

* multi language survey
* multi language admin
* rtf report including analysis
* csv export
* configurable timeouts, presets, colour palette
* partially configurable borders

exports will be stored within the documents-folder with a timestamp in the filename. on pc as well as on android device.

supported languages dependent on used fonts. cyrillic works, arabic does not by default.

*disclaimer and most probably wontfixes:*
* no warranty on russian. automated web translations have been proofread by a native speaker once. could still insult your mother. idk.
* csv-fields are enclosed in double quotes with proper escaping. works fine on desktop excel 2016 but not neccessarily on mobile ms office 365
* the csv-export does not provide the actual queried ratings but the database columns RATING0-3 instead. this does not matter that much for the rtf-analysis is suitable enough regarding quality management topics.  

![screenshot](https://raw.githubusercontent.com/erroronline1/customersurvey.py/master/images/screenshot.png)

## usage

* once compiled using buildozer install the apk on the device
* on initial start the database will be initialized. you will be asked to provide a password. do not forget this, for you will have to provide it to access any admin options, including data export. if you loose the password only removing and reinstalling the app will make it usable again.
* on each start of the app there will be an csv-export. in case you really forget the password you could still restart the app and analyze the database dump by hand, so at least not all data is lost. might junk up the documents folder in the long run but the intended use is to run 24/7 anyway.
* you can set the timeout, colour palette and default languages for your audience
* you can set up border spacings to some amount to match possible frames for the device

most settings take effect only after restarting the app. 

## code-features

* handling of environment, desktop by default, android by conditional platform
* language easily extendable within own module
* questions can be modified within the language module. the database doesn't care. provided questions will be implemented within the report. requires a new compiling process though

sorry for the excitement, but i'm just freaking glad it works w/o needing to learn java. i'm not totally sure about every buildozer.spec setting, but it works now.

tested on Samsung Galaxy S9 @ Android10, Samsung Galaxy S10 @ Android12, Lenovo M10 @ Android 11

## resources

1. Mariyas youtube-video on [Convert Python to Android with WINDOWS & LINUX + Fix Common Bugs](https://www.youtube.com/watch?v=VsTaM057rdc)
2. explanations on [private storage handling](https://github.com/Android-for-Python/Android-for-Python-Users#private-storage)
3. rescue on [cross-api storage handling](https://github.com/Android-for-Python/androidstorage4kivy)

