# -*- coding: utf-8 -*-
import sqlite3
from language import Language

class DataBase():
	tableFields = {
		"CS": ["ID", "DATE", "RATING", "RATING0", "RATING1", "RATING2", "RATING3", "COMMENDATION", "SUGGESTION", "SERVICE"],
		"SETTING": ["KEY", "VALUE"]
	}
	password = ""
	status = ""
	def __init__(self, db, exportpath = None):
		self.exportPath = exportpath
		# tries to establish connection, creates on fail.
		try:
			self.connection = sqlite3.connect(db)
			c = self.connection.cursor()
			c.execute(f'''
				CREATE TABLE IF NOT EXISTS CS
				({self.tableFields["CS"][0]} INTEGER PRIMARY KEY AUTOINCREMENT,
				{self.tableFields["CS"][1]} TINYTEXT,
				{self.tableFields["CS"][2]} INTEGER,
				{self.tableFields["CS"][3]} INTEGER,
				{self.tableFields["CS"][4]} INTEGER,
				{self.tableFields["CS"][5]} INTEGER,
				{self.tableFields["CS"][6]} INTEGER,
				{self.tableFields["CS"][7]} TEXT,
				{self.tableFields["CS"][8]} TEXT,
				{self.tableFields["CS"][9]} TINYTEXT);''')
			c.execute(f'''
				CREATE TABLE IF NOT EXISTS SETTING
				({self.tableFields["SETTING"][0]} TINYTEXT UNIQUE,
				{self.tableFields["SETTING"][1]} TINYTEXT);''')
			self.connection.commit()
			
			getpwd = self.read(["VALUE"], "SETTING", {"KEY":"password"})
			self.password = getpwd[0][0] if getpwd else ''
		except Exception as error:
			self.status +=f" {error} {db}"

	def __del__(self):
		self.connection.close()

	def write(self, table="", key_value={}, where={}):
		condition, values, updates = [], [], []
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		for column in self.tableFields[table]:
			if column in key_value:
				values.append(f"{self.sanitize(key_value[column])}")
				updates.append(f"{column}={self.sanitize(key_value[column])}")
			else:
				values.append("NULL")
		# try to update exsting
		if len(condition):
			self.connection.execute(f"UPDATE {table} SET {', '.join(updates)} WHERE {' AND '.join(condition)};")
		# otherwise insert
		self.connection.execute(f"INSERT OR IGNORE INTO {table} ({', '.join(self.tableFields[table])}) VALUES ({', '.join(values)});")
		self.connection.commit()

		if table=="CS":
			# keep track of latest insert_id to have rows updated instead of appended if submitted
			cursor = self.connection.cursor()
			cursor.execute(f"SELECT MAX(ID) FROM CS;")
			result = cursor.fetchone()
			if result is not None:
				return result[0]
		return True

	def read(self, fields = [], table = "", where = {}):
		condition, fields = [], [self.sanitize(field, False) for field in fields] if fields else "*"
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT {' AND '.join(fields)} FROM {table} WHERE {' AND '.join(condition)};")
		result = cursor.fetchall()
		if result is not None:
			return result
		return False

	def delete(self, table = "", where = {}):
		condition= []
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		if len(condition):
			self.connection.execute(f"DELETE FROM {table} WHERE {' AND '.join(condition)};")
		self.connection.commit()
		return True

	def sanitize(self, value = "", quotes = True):
		# sanitary strings to concatenate to sql queries.
		# if not quotes it probbly is a column key
		if type(value)==str and value != "NULL":
			if value.strip()=="":
				return "NULL"
			return value.replace('\'','\'\'') if not quotes else "'" + value.replace('\'','\'\'') + "'"
		return value

	def clear(self, tables=[]):
		# reset database
		for table in tables:
			self.connection.executescript(f"DELETE FROM {table}; VACUUM;")
		self.connection.commit()
		return True

	def rtf(self, language):
		# create a report
		text = Language(language)
		rtfHead = text.get("rtfHead")
		rtfTotal = text.get("rtfTotal")
		rtfDetail = text.get("rtfDetail")
		rtfTextInput = text.get("rtfTextInput")
		rtfCommendation = text.get("commendationLabel")
		rtfSuggestion = text.get("suggestionLabel")

		output = "{\\rtf1 \\ansi\\ansicpg1252\\deff0\\nouicompat "

		# total and main review
		cursor = self.connection.cursor()
		cursor.execute("SELECT MIN(DATE) AS zero, MAX(DATE) AS one, COUNT(ID) AS two, AVG(RATING) AS three FROM CS;")
		result = cursor.fetchall()
		if result is None:
			return False
		result = result[0]
		
		output += f"{{\\b {rtfHead[0]} {result[0]} {rtfHead[1]} {result[1]}}} \par "
		output += f"{{\\b {rtfTotal[0]}:}} "
		output += f"\line {rtfTotal[1]} {result[0]} {rtfTotal[2]} {result[1]} {rtfTotal[3]} {result[2]} {rtfTotal[4]} {round(result[3]*50, 2)} % \par "
		
		# topic related statistics
		details = [text.get("detailratingAvailability"), text.get("detailratingProcessing"), text.get("detailratingExpertise"), text.get("detailratingKindness")]
		for i, detail in enumerate(details):
			cursor.execute(f"SELECT MIN(DATE) AS zero, MAX(DATE) AS one, COUNT(ID) AS two, AVG(RATING{i}) AS three FROM CS WHERE RATING{i} IS NOT NULL;")
			result = cursor.fetchall()
			if result is None:
				output += f"\par {{\i {detail}}} {rtfDetail[5]} \line "
				continue
			result = result[0]
			output += f"\par {rtfDetail[0]} {{\i {detail}}} "
			output += f"\line {rtfDetail[1]} {result[0]} {rtfDetail[2]} {result[1]} {rtfDetail[3]} {result[2]} {rtfDetail[4]} {round(result[3]*50, 2)if result[3] else None} %"

		# customer text inputs
		rating = [text.get("detailratingBad"), text.get("detailratingMeh"), text.get("detailratingGood")]
		output += f"\par \line {{\\b {rtfTextInput[0]}}} "
		cursor.execute("SELECT * FROM CS WHERE COMMENDATION IS NOT NULL OR SUGGESTION IS NOT NULL OR SERVICE IS NOT NULL;")
		result = cursor.fetchall()
		if result is None:
			output += f"{rtfTextInput[2]}"
		else:
			for r in result:
				output += f"\par \line {{\\b {r[1]}}} {r[9] if r[9] else ''} \line "
				output += f"{{\i {rtfCommendation}:}} {r[7]} \line " if r[7] != None else ""
				output += f"{{\i {rtfSuggestion}:}} {r[8]} \line " if r[8] != None else ""
				for i, detail in enumerate(details):
					output += f"{detail}: {rating[r[3+i]]} / " if r[3+i] != None else ""
				output += f"{rtfTextInput[1]}: {rating[r[2]]} "
		
		output +="}"
		try:
			with open(self.exportPath, 'w', newline = '') as rtfFile:
				rtfFile.write(output)
			self.status = self.exportPath
			return True
		except Exception as error:
			self.status = error
			return False