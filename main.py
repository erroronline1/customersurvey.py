__version__ = "0.1"

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock

from lang import language
import database

from kivy.core.window import Window

'''
todo

timeout
admin export
'''

class IconListItem(OneLineIconListItem):
	icon = StringProperty()

class ContentNavigationDrawer(MDBoxLayout):
	screen_manager = ObjectProperty()
	nav_drawer = ObjectProperty()

class CustomersurveyApp(MDApp): # <- main class
	dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.selectedLanguage = "deutsch"
		self.theme_cls.theme_style = "Light"
		self.theme_cls.primary_palette = "Teal"

		self.database = database.DataBase(self.user_data_dir + "/CustomerSurvey.db")
		self.screen = Builder.load_file("layout.kv")

	def __getitem__(self, x):
		return getattr(self, x)

	def build(self):
		Window.size = (400, 666) #1200x2000 samsung galaxy tab a7
		dropdown_options  =self.dropdown_options()
		self.ratingDropdown = self.dropdown_generator(dropdown_options["rating"])
		self.languageDropdown = self.dropdown_generator(dropdown_options["language"])
		if not self.database.password:
			self.notif(self.content("initMessage"), 1)
			self.screen.children[0].children[1].current = "evaluateScreen"
		return self.screen

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
				"context": "ratingDropdown"
			},
			"language":{
				"options": [{"icon": "translate", "option": l} for l in language()],
				"fields": ["languageSelection"],
				"context": "languageDropdown"
			}
		}

	def dropdown_generator(self, parameter):
		items = [
			{
				"text": self.content(i["content"]) if "content" in i else i["option"],
				"content":i["content"] if "content" in i else None,
				"height": dp(64),
				"viewclass": "IconListItem" if "icon" in i else None,
				"icon": i["icon"] if "icon" in i else None,
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

	def notif(self, msg, delay = 0):
		def sb(this):
			Snackbar(
				text = msg,
				snackbar_x = "10dp",
				snackbar_y = "10dp",
				size_hint_x = (
					Window.width - (dp(10) * 2)
				) / Window.width
			).open()
		Clock.schedule_once(sb, delay)

	def confirm_reset(self):
		if not self.dialog:
			self.dialog = MDDialog(
				text = self.content("buttonReset"),
				buttons = [
					MDFlatButton(
						text = self.content("cancelReset"),
						on_release = lambda btnObj: self.dialog.dismiss()
						#theme_text_color="Custom",
						#text_color=self.theme_cls.primary_color,
					),
					MDFlatButton(
						text = self.content("confirmReset"),
						on_release = self.reset_confirmed
						#theme_text_color="Custom",
						#text_color=self.theme_cls.primary_color,
					),
				],
			)
		self.dialog.open()

	def reset_confirmed(self, *args):
		self.dialog.dismiss()
		self.database.clear(["CS", "SETTING"])
		self.notif(self.content("resetMessage"))


	def content(self, element):
		return language(element, self.selectedLanguage)

	def translate(self, lang):
		allElements = language(None, None, True)
		self.selectedLanguage = lang 
		for element in allElements:
			try:
				# not all language chunks have their respective id'd counterparts like
				# * dropdown-objects detailratingGood, -Meh and -Bad
				self.screen.ids[element].text = allElements[element][lang]
			except:
				continue
		# exceptions for dropdowns
		dropdown_options=self.dropdown_options()
		for field in dropdown_options["rating"]["fields"]:
			self.screen.ids[field].text = allElements["detailratingSelect"][lang]
			self.ratingDropdown[field].items = [dict(
				item,
				**{"text":allElements[item["content"]][lang]} if item["content"] else {},
				**{"on_release": lambda x = (field, allElements[item["content"]][lang], dropdown_options["rating"]["context"]): self.select_dropdown_item(x[0], x[1], x[2])} if item["content"] else {}
				) for item in self.ratingDropdown[field].items]

	def on_stop(self):
		#without this, app will not exit even if the window is closed
		pass

if __name__ == "__main__":
	CustomersurveyApp().run()
