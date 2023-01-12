# -*- coding: utf-8 -*-
__version__ = "1.0"

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock

import os
from datetime import datetime

from language import Language
from platformhandler import platform_handler
import database

class IconListItem(OneLineIconListItem):
	icon = StringProperty()

class ContentNavigationDrawer(MDBoxLayout):
	screen_manager = ObjectProperty()
	nav_drawer = ObjectProperty()

class CustomerSurveyApp(MDApp): # <- main class
	dialog = None
	session = "NULL" # according to database id to assign inputs to a row
	initialRating = None
	timeout = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.platform = platform_handler()
		self.database = database.DataBase(os.path.join( self.platform.app_dir, "CustomerSurvey.db"))

		timeout = self.database.read(["VALUE"], "SETTING", {"KEY": "timeout"})
		self.timeoutSeconds = int(timeout[0][0] if timeout else 30)
		theme=self.database.read(["VALUE"], "SETTING", {"KEY": "theme"})
		self.theme_cls.primary_palette = theme[0][0] if theme else self.theme_cls.primary_palette
		surveylanguage = self.database.read(["VALUE"], "SETTING", {"KEY": "surveylanguage"})
		adminlanguage = self.database.read(["VALUE"], "SETTING", {"KEY": "adminlanguage"})
		self.text = Language(surveylanguage[0][0] if surveylanguage else None, adminlanguage[0][0] if adminlanguage else None)
		resetLanguageonRestart = self.database.read(["VALUE"], "SETTING", {"KEY": "resetsurveylanguage"})
		self.resetLanguage = (bool(int(resetLanguageonRestart[0][0])) if resetLanguageonRestart else True)

		if self.platform.window_size:
			Window.size = self.platform.window_size
		self.screen_adjustments()
		self.screen = Builder.load_file("layout.kv")

	def __getitem__(self, x):
		return getattr(self, x)

	def build(self):
		self.icon = r'assets/app_icon.png'
		dropdown_options = self.dropdown_options()
		self.surveyRatingDropdown = self.dropdown_generator(dropdown_options["rating"], "survey")
		self.surveySurveyLanguageDropdown = self.dropdown_generator(dropdown_options["surveySurveyLanguage"], "survey")
		self.adminSurveyLanguageDropdown = self.dropdown_generator(dropdown_options["adminSurveyLanguage"], "survey")
		self.adminLanguageDropdown = self.dropdown_generator(dropdown_options["adminAdminLanguage"], "admin")
		self.adminThemeDropdown = self.dropdown_generator(dropdown_options["theme"], "admin")
		if not self.database.password:
			self.screen.children[0].children[1].current = "adminScreen"
		return self.screen

	def screen_adjustments(self):
		layout = (self.database.read(["VALUE"], "SETTING", {"KEY": "paddingleft"}),
			self.database.read(["VALUE"], "SETTING", {"KEY": "paddingtop"}),
			self.database.read(["VALUE"], "SETTING", {"KEY": "paddingright"}),
			self.database.read(["VALUE"], "SETTING", {"KEY": "paddingbottom"}),
			self.database.read(["VALUE"], "SETTING", {"KEY": "topbar"}))
		self.layout = {"left": int(layout[0][0][0] if layout[0] else 20),
			"top": int(layout[1][0][0] if layout[1] else 0),
			"right": int(layout[2][0][0] if layout[2] else 20),
			"bottom": int(layout[3][0][0] if layout[3] else 20),
			"topbar": int(layout[4][0][0] if layout[4] else 10) / 100,
			}

	def dropdown_options(self):
		return {
			"rating":{
				"options": [
					{"icon": "emoticon-happy-outline", "content": "detailratingGood"},
					{"icon": "emoticon-neutral-outline", "content": "detailratingMeh"},
					{"icon": "emoticon-sad-outline", "content": "detailratingBad"}
				],
				"fields": [
					"detailratingQone",
					"detailratingQtwo",
					"detailratingQthree",
					"detailratingQfour"
				],
				"context": "surveyRatingDropdown"
			},
			"surveySurveyLanguage":{
				"options": [{"icon": "translate", "option": l} for l in self.text.available("survey")],
				"fields": ["surveySurveyLanguageSelection"],
				"context": "surveySurveyLanguageDropdown"
			},
			"adminSurveyLanguage":{
				"options": [{"icon": "translate", "option": l} for l in self.text.available("survey")],
				"fields": ["adminSurveyLanguageSelection"],
				"context": "adminSurveyLanguageDropdown"
			},
			"adminAdminLanguage":{
				"options": [{"icon": "translate", "option": l} for l in self.text.available("admin")],
				"fields": ["adminLanguageSelection"],
				"context": "adminLanguageDropdown"
			},
			"theme":{
				"options": [{"icon": "palette", "option": l} for l in ["Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue", "LightBlue", "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow", "Amber", "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"]],
				"fields": ["adminThemeSelection"],
				"context": "adminThemeDropdown"
			},			
		}

	def dropdown_generator(self, parameter, context):
		con_text = getattr(self.text, context)
		items = [
			{
				"text": con_text(i["content"]) if "content" in i else i["option"],
				"content": i.get("content"),
				"height": dp(64),
				"viewclass": "IconListItem" if "icon" in i else None,
				"icon": i.get("icon")
			} for i in parameter["options"]
		]
		return {
			field: MDDropdownMenu(
					caller = self.screen.ids[field],
					items = [dict(i,
						**{"on_release": lambda x = (field, i["text"], parameter["context"]): self.select_dropdown_item(x[0], x[1], x[2])}
						) for i in items],
					position = "center",
					width_mult = 4
			) for field in parameter["fields"]
		}

	def select_dropdown_item(self, field, text, context):
		self.screen.ids[field].text = text
		self[context][field].dismiss()

	def notif(self, msg, display_delayed = 0):
		def sb(this):
			Snackbar(
				text = msg,
				snackbar_x = self.layout["left"],
				snackbar_y = self.layout["bottom"],
				size_hint_x = (Window.width - self.layout["left"] - self.layout["right"]) / Window.width,
			).open()
		Clock.schedule_once(sb, display_delayed)

	def cancel_confirm_dialog(self, decision, cancel, confirm):
		if not self.dialog:
			self.dialog = MDDialog(
				text = decision,
				buttons = [
					MDFlatButton(
						text = cancel,
						on_release = self.cancel_confirm_dialog_handler
					),
					MDFlatButton(
						text = confirm,
						on_release = self.cancel_confirm_dialog_handler
					),
				],
			)
		self.dialog.open()

	def cancel_confirm_dialog_handler(self, *btnObj):
		self.dialog.dismiss()
		if btnObj[0].text == self.text.admin("confirmReset"):
			self.database.clear(["CS", "SETTING"])
			self.notif(self.text.admin("resetMessage"))

	def translate(self, lang, context):
		for element in self.text.elements[context]:
			try:
				# not all language chunks have their respective id'd counterparts like
				# * dropdown-objects detailratingGood, -Meh and -Bad
				obj = self.screen.ids[element]
				if hasattr(obj, "hint_text") and obj.hint_text:
					obj.hint_text = self.text.elements[context][element][lang]
				elif hasattr(obj, "text") and obj.text:
					obj.text = self.text.elements[context][element][lang]
			except:
				continue
		if context=="survey":
			self.text.currentSurveyLanguage = lang
			# exceptions for dropdowns
			dropdown_options=self.dropdown_options()
			for field in dropdown_options["rating"]["fields"]:
				self.screen.ids[field].text = self.text.elements[context]["detailratingSelect"][lang]
				self.surveyRatingDropdown[field].items = [dict(
					item,
					**{"text": self.text.elements[context][item["content"]][lang]} if item["content"] else {},
					**{"on_release": lambda x = (field, self.text.elements[context][item["content"]][lang], dropdown_options["rating"]["context"]): self.select_dropdown_item(x[0], x[1], x[2])} if item["content"] else {}
					) for item in self.surveyRatingDropdown[field].items]
		else:
			self.text.adminLanguage = lang
		# exception for toolbar
		self.screen.ids["toolbar"].title=self.text.survey("menuSurvey" if self.screen.children[0].children[1].current == "surveyScreen" else "menuAdmin")

	def timeout_handler(self, event = None):
		if self.timeout is not None:
			self.timeout.cancel()
		if event == "stop":
			self.timeout = None
			return
		self.timeout = Clock.schedule_once(self.restart, self.timeoutSeconds)

	def restart(self, *args):
		if self.screen.children[0].children[1].current == "adminScreen":
			return
		self.save_inputs()
		# reset all values and fields
		self.initialRating = None
		self.session = "NULL"
		for field in self.dropdown_options()["rating"]["fields"]:
			self.screen.ids[field].text = self.text.survey("detailratingSelect")
		for field in ["commendation", "suggestion", "service"]:
			self.screen.ids[field].text = ""

		if self.resetLanguage and self.text.currentSurveyLanguage != self.text.defaultSurveyLanguage:
			self.text.currentSurveyLanguage = self.text.defaultSurveyLanguage
			self.translate(self.text.currentSurveyLanguage, "survey")
		# goto initial slide
		sc=self.screen.children[0].children[1].children[0].children[0]
		sc.load_slide(sc.slides[0])

	def save_inputs(self):
		if self.initialRating is not None:
			# process all possible fields. slidewise is unreliable and skips occasionally
			now = datetime.now()
			key_value = {
				"ID": self.session,
				"DATE": now.strftime("%Y-%m-%d"),
				"RATING": self.initialRating,
				"COMMENDATION": self.screen.ids["commendation"].text if self.screen.ids["commendation"].text else "NULL",
				"SUGGESTION": self.screen.ids["suggestion"].text if self.screen.ids["suggestion"].text else "NULL",
				"SERVICE": self.screen.ids["service"].text if self.screen.ids["service"].text else "NULL"
				}
			dropdown_options = self.dropdown_options()
			grades = [self.text.survey("detailratingBad"), self.text.survey("detailratingMeh"), self.text.survey("detailratingGood")]
			for i, field in enumerate(dropdown_options["rating"]["fields"]):
				if self.screen.ids[field].text in grades:
					key_value[f'RATING{i}'] = grades.index(self.screen.ids[field].text)
			self.session = self.database.write("CS", key_value, {"ID": self.session})
		else:
			self.notif(self.text.survey("missingRateNotif"))

	def save_setting(self, key, value):
		sanitize={
			"default": lambda x: int(x),
			"password": lambda x: x.strip(),
			"theme": lambda x: x.strip(),
			"surveylanguage": lambda x: x.strip(),
			"adminlanguage": lambda x: x.strip(),
			"resetsurveylanguage": lambda x: int(x),
			"topbar": lambda x: int(float(x)) if 7 < int(float(x)) < 16 else 10,
			"timeout": lambda x: int(x) if int(x) > 5 else 5 # even though this fallback is rather short
		}
		try:
			if key in sanitize:
				value=sanitize[key](value)
			else:
				value=sanitize["default"](value)
		except Exception as e:
			value=""
		if value in ("", "NULL"):
			self.database.delete("SETTING", {"KEY": key})
		else:
			self.database.write("SETTING", {"KEY": key, "VALUE": value}, {"KEY": key})
		return str(value)

	def export(self, type="rtf"):
		now = datetime.now()
		timestamp = now.strftime("%Y-%m-%d_%H-%M")
		if type=="rtf":
			content = self.database.rtf(self.text.adminLanguage)
			success = self.platform.fileExport(f"CustomerSurvey_{timestamp}.rtf", content)
			self.notif(f"{self.text.admin('rtfSuccess' if success['success'] else 'rtfFail')} {success['return']}")
		elif type=="csv":
			content = self.database.csv()
			success = self.platform.fileExport(f"CustomerSurvey_{timestamp}.csv", content)
			self.notif(f"{self.text.admin('csvSuccess' if success['success'] else 'csvFail')} {success['return']}")

	def on_stop(self):
		#without this, app will not exit even if the window is closed
		pass

if __name__ == "__main__":
	CustomerSurveyApp().run()
