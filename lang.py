# -*- coding: utf-8 -*-
# user interface and default values

def language(chunk=None, lang=None, update=None):
	element={
		"menuFeedback": {
			"english": "Survey",
			"deutsch": "Umfrage"
		},
		"menuEvaluate": {
			"english": "Evaluate",
			"deutsch": "Auswerten"
		},

		"welcomeLabel": {
			"english": "What is your opinion?",
			"deutsch": "Wie zufrieden sind Sie mit uns?"
		},

		"missingRateNotif":{
			"english": "Please provide you general opinion :)",
			"deutsch": "Bitte geben Sie ihren Gesamteindruck an :)"
		},

		"encouragementLabel": {
			"english": "Thank you for your opinion!",
			"deutsch": "Danke für Ihre Meinung!"
		},
		"encouragementText": {
			"english": "We would be glad if you take a little more of your time. Do you mind answering a few more questions? Of course all statements are optional!",
			"deutsch": "Wir freuen uns, wenn Sie noch einen kleinen Moment Zeit für uns haben. Beantworten Sie uns noch ein paar Fragen? Alle Angaben sind selbstverständlich freiwillig!"
		},
		"encouragementYes": {
			"english": "yes of course",
			"deutsch": "ja klar"
		},
		"encouragementNo": {
			"english": "no thank you",
			"deutsch": "nein danke"
		},

		"detailratingLabel": {
			"english": "How did you experience your treatment?",
			"deutsch": "Wie empfanden Sie die Versorgung mit Ihrem Hilfsmittel?"
		},
		"detailratingAvailability": {
			"english": "Staff availability",
			"deutsch": "Erreichbarkeit"
		},
		"detailratingProcessing": {
			"english": "Processing time",
			"deutsch": "Bearbeitungszeit"
		},
		"detailratingExpertise": {
			"english": "Expertise",
			"deutsch": "Kompetenz"
		},
		"detailratingKindness": {
			"english": "Kindness",
			"deutsch": "Freundlichkeit"
		},
		"detailratingGood": {
			"english": "good",
			"deutsch": "gut"
		},
		"detailratingMeh": {
			"english": "meh",
			"deutsch": "so la la"
		},
		"detailratingBad": {
			"english": "bad",
			"deutsch": "schlecht"
		},
		"detailratingSelect": {
			"english": "rate",
			"deutsch": "bewerten"
		},

		"commendationLabel": {
			"english": "What has been positive?",
			"deutsch": "Was hat Ihnen gefallen?"
		},

		"suggestionLabel": {
			"english": "How can we improve?",
			"deutsch": "Was können wir besser machen?"
		},

		"serviceLabel": {
			"english": "Which aid did you receive?",
			"deutsch": "Welches Hilfsmittel haben Sie von uns erhalten?"
		},

		"textHint":{
			"english": "Text",
			"deutsch": "Text"

		},

		"thankyouLabel": {
			"english": "Thank you for your time!",
			"deutsch": "Vielen Dank für Ihre Zeit!"
		},
		"thankyouRestart": {
			"english": "restart",
			"deutsch": "von vorne"
		},

		"adminPass": {
			"english": "password",
			"deutsch": "Kennwort"
		},
		"buttonPassword": {
			"english": "set password",
			"deutsch": "Kennwort festlegen"
		},
		"buttonExport": {
			"english": "export",
			"deutsch": "exportieren"
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
		"devInfo": {
			"english": '''customer survey by error on line 1 (erroronline.one)

server- and cloudless, privacy oriented solution.
visit the open source code on github.com/erroronline1/customersurvey.py''',
			"deutsch": '''Kundenumfrage von error on line 1 (erroronline.one)
server- und cloudlos, datenschutzorientierte Lösung.
Besuche den offenen Quelltext auf github.com/erroronline1/customersurvey.py'''
		},

		"initMessage": {
			"english": "database initialized...",
			"deutsch": "Datenbank initialisiert..."
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
	}
	if chunk and chunk not in element:
		return "This content snippet has not been declared yet"
	if update:
		return element
	if not chunk and not lang:
		return tuple(key for key in element["welcomeLabel"])
	return element[chunk][lang] if lang in element[chunk] else element[chunk]["english"]