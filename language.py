# -*- coding: utf-8 -*-
import random

class Language():
	# text chunks. extend elements at your convenience
	elements={
		"survey":{
			"menuSurvey": {
				"english": "Survey",
				"deutsch": "Umfrage",
				"русский": "Опрос",
			},
			"menuAdmin": {
				"english": "Settings",
				"deutsch": "Einstellungen",
				"русский": "Настройки",
			},

			"welcomeLabel": {
				"english": "How satisfied are you with us?",
				"deutsch": "Wie zufrieden sind Sie mit uns?",
				"русский": "Насколько Вы довольны нами?",
			},

			"missingRateNotif":{
				"english": "Please provide you general opinion :)",
				"deutsch": "Bitte geben Sie ihren Gesamteindruck an :)",
				"русский": "Пожалуйста укажите Ваше общее впечатление :)",
			},

			"encouragementLabel": {
				"english": "Thank you for your opinion!",
				"deutsch": "Danke für Ihre Meinung!",
				"русский": "Спасибо за Ваше мнение!",
			},
			"encouragementText": {
				"english": "We would be delighted if you could spare a few minutes for us. Do you mind answering a few more questions? Of course all statements are optional!",
				"deutsch": "Wir freuen uns, wenn Sie noch einen kleinen Moment Zeit für uns haben. Beantworten Sie uns noch ein paar Fragen? Alle Angaben sind selbstverständlich freiwillig!",
				"русский": "Мы будем рады, если Вы уделите нам несколько минут. Не могли бы Вы ответить еще на несколько вопросов? Вся информация разумеется является добровольной!",
			},
			"encouragementYes": {
				"english": "yes of course",
				"deutsch": "ja klar",
				"русский": "Да конечно",
			},
			"encouragementNo": {
				"english": "no thank you",
				"deutsch": "nein danke",
				"русский": "Нет, спасибо",
			},

			"detailratingLabel": {
				"english": "How did you experience your treatment?",
				"deutsch": "Wie empfanden Sie die Versorgung mit Ihrem Hilfsmittel?",
				"русский": "Как Вы оцениваете наше обслуживание в процессе изготовления для Вас ортопедического вспомогательного средства?",
			},
			"detailratingAvailability": {
				"english": "Staff availability",
				"deutsch": "Erreichbarkeit",
				"русский": "Доступность",
			},
			"detailratingProcessing": {
				"english": "Processing time",
				"deutsch": "Bearbeitungszeit",
				"русский": "Время обработки",
			},
			"detailratingExpertise": {
				"english": "Expertise",
				"deutsch": "Kompetenz",
				"русский": "компетентность",
			},
			"detailratingKindness": {
				"english": "Kindness",
				"deutsch": "Freundlichkeit",
				"русский": "доброжелательность",
			},
			"detailratingGood": {
				"english": "good",
				"deutsch": "gut",
				"русский": "хорошо",
			},
			"detailratingMeh": {
				"english": "meh",
				"deutsch": "so la la",
				"русский": "посредственно",
			},
			"detailratingBad": {
				"english": "bad",
				"deutsch": "schlecht",
				"русский": "плохо",
			},
			"detailratingSelect": {
				"english": "rate",
				"deutsch": "bewerten",
				"русский": "оценить",
			},

			"commendationLabel": {
				"english": "What has been positive?",
				"deutsch": "Was hat Ihnen gefallen?",
				"русский": "Что вам понравилось?",
			},

			"suggestionLabel": {
				"english": "How can we improve?",
				"deutsch": "Was können wir besser machen?",
				"русский": "Что по Вашему мнению мы можем улучшить в обслуживании?",
			},

			"serviceLabel": {
				"english": "Which aid did you receive?",
				"deutsch": "Welches Hilfsmittel haben Sie von uns erhalten?",
				"русский": "Какое ортопедическое вспомогательное средство Вы получили в нашей клинике?",
			},

			"textHint":{
				"english": "Text",
				"deutsch": "Text",
				"русский": "Текст",
			},

			"thankyouLabel": {
				"english": "Thank you for your time!",
				"deutsch": "Vielen Dank für Ihre Zeit!",
				"русский": "Спасибо, что уделили нам время!",
			},
			"thankyouRestart": {
				"english": "restart",
				"deutsch": "von vorne",
				"русский": "сначала",
			},
		},
		"admin": {
			"adminPass": {
				"english": "confirmation password",
				"deutsch": "Kennwort zur Bestätigung"
			},
			"buttonPassword": {
				"english": "set password",
				"deutsch": "Kennwort festlegen"
			},
			"buttonRtfExport": {
				"english": "generate RTF report",
				"deutsch": "RTF Analyse erzeugen"
			},
			"buttonCsvExport": {
				"english": "export CSV data",
				"deutsch": "CSV Datenexport"
			},
			"buttonReset": {
				"english": "reset",
				"deutsch": "zurücksetzen"
			},
			"cancelReset":{
				"english": "ooops, no!",
				"deutsch": "Hoppla, nein!"
			},
			"confirmReset":{
				"english": "I'm sure",
				"deutsch": "Ich bin mir sicher"
			},

			"initMessage": {
				"english": "Database initialized. Please provide password.",
				"deutsch": "Datenbank initialisiert. Bitte Kennwort angeben."
			},
			"resetMessage": {
				"english": "please restart app...",
				"deutsch": "App bitte neu starten..."
			},

			"rtfHead":{
				"english": ["Customer Survey Report based on disclosures from", "until"],
				"deutsch": ["Kundenzufriedenheitsanalyse basierend auf den Angaben von", "bis"]
			},
			"rtfTotal":{
				"english": ["Total Rating", "From", "until", "", "general votes result in a satisfaction rate of"],
				"deutsch": ["Gesamteinschätzung", "Von", "bis", "ergeben", " allgemeine Bewertungen eine Zufriedenheit von"]
			},
			"rtfDetail":{
				"english": ["Regarding", "From", "until", "", "votes result in a satisfaction rate of", "has not been answered yet"],
				"deutsch": ["In der Fragestellung", "Von", "bis", "ergeben", "allgemeine Bewertungen eine Zufriedenheit von", "wurde noch nicht beantwortet"]
			},
			"rtfTextInput":{
				"english": ["Commendations and suggestions", "general rating", "have not been provided yet"],
				"deutsch": ["Lob und Vorschläge", "allgemeine Bewertung", "sind noch nicht abgegeben worden"]
			},
			"rtfFail":{
				"english": "Report could not be generated",
				"deutsch": "Analyse konnte nicht erstellt werden."
			},
			"rtfSuccess":{
				"english": "Report saved as",
				"deutsch": "Analyse gespeichert unter"
			},
			"csvFail":{
				"english": "Export could not be generated",
				"deutsch": "Export konnte nicht erstellt werden."
			},
			"csvSuccess":{
				"english": "Export saved as",
				"deutsch": "Export gespeichert unter"
			},

			"adminTimeout": {
				"english": "Timeout",
				"deutsch": "Zeitablauf"
			},
			"adminThemeSelectionLabel":{
				"english": "color scheme",
				"deutsch": "Farbschema"
			},
			"surveyLanguageSelectionLabel":{
				"english": "default survey language",
				"deutsch": "Standardsprache Umfrage"
			},
			"surveyLanguageResetLabel":{
				"english": "default language on restart",
				"deutsch": "Standardsprache bei Neustart"
			},
			"adminLanguageSelectionLabel":{
				"english": "default admin language",
				"deutsch": "Standardsprache Auswertung"
			},

			"adminScreenTopBarPercent": {
				"english": "Top bar height in percent",
				"deutsch": "Höhe des oberen Menübalkens in Prozent"
			},
			"adminScreenPaddingLeft": {
				"english": "left padding",
				"deutsch": "Randabstand links"
			},
			"adminScreenPaddingTop": {
				"english": "top padding",
				"deutsch": "Randabstand oben"
			},
			"adminScreenPaddingRight": {
				"english": "right padding",
				"deutsch": "Randabstand rechts"
			},
			"adminScreenPaddingBottom": {
				"english": "bottom padding",
				"deutsch": "Randabstand unten"
			},
			"adminSave": {
				"english": "save",
				"deutsch": "speichern"
			},

			"devInfo": {
				"english": '''customer survey by error on line 1 (erroronline.one)

cloudless, privacy oriented.

inputs are exclusively stored locally.
''',
				"deutsch": '''Kundenumfrage von error on line 1 (erroronline.one)

Cloudlos, datenschutzorientiert.

Eingaben werden ausschließlich lokal auf dem Gerät gespeichert.
'''
			},
		}
	}
	def __init__(self, surveylanguage = None, adminlanguage = None):
		# define selected language, defaults to first available language
		self.defaultSurveyLanguage = surveylanguage if surveylanguage in self.available("survey") else self.available("survey")[0]
		self.currentSurveyLanguage = self.defaultSurveyLanguage
		self.adminLanguage = adminlanguage if adminlanguage in self.available("admin") else self.available("admin")[0]
	def available(self, what):
		# tuple of all defined languages for what
		return tuple(key for key in self.elements[what][random.choice(list(self.elements[what].keys()))])
	def survey(self, chunk):
		# returns requested element for survey
		result = self.elements["survey"].get(chunk)
		return result[self.currentSurveyLanguage] if result else "This content snippet has not been declared yet"
	def admin(self, chunk):
		# returns requested element for admin
		result = self.elements["admin"].get(chunk)
		return result[self.adminLanguage] if result else "This content snippet has not been declared yet"