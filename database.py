import sqlite3

class DataBase():
	tableFields = {
		"CS": ["ID", "DATE", "RATING", "RATING0", "RATING1", "RATING2", "RATING3", "COMMENDATION", "SUGGESTION", "SERVICE"],
		"SETTING": ["KEY", "VALUE"]
	}
	password = ''
	def __init__(self, db):
		try:
			self.connection = sqlite3.connect(db)
			c = self.connection.cursor()
			c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CS';")
			if not c.fetchone()[0]:
				self.create()
			else:
				getpwd = self.read("SETTING", {"KEY":"password"})
				self.password = getpwd[0][1] if getpwd else ''
		except Exception as error:
			pass

	def __del__(self):
		self.connection.close()

	def create(self):
		self.connection.executescript(f'''
			CREATE TABLE CS
			({self.tableFields["CS"][0]} INTEGER PRIMARY KEY AUTOINCREMENT,
			{self.tableFields["CS"][1]} TINYTEXT,
			{self.tableFields["CS"][2]} INTEGER,
			{self.tableFields["CS"][3]} INTEGER,
			{self.tableFields["CS"][4]} INTEGER,
			{self.tableFields["CS"][5]} INTEGER,
			{self.tableFields["CS"][6]} INTEGER,
			{self.tableFields["CS"][7]} TEXT,
			{self.tableFields["CS"][8]} TEXT,
			{self.tableFields["CS"][9]} TINYTEXT);

			CREATE TABLE SETTING
			({self.tableFields["SETTING"][0]} TINYTEXT UNIQUE,
			{self.tableFields["SETTING"][1]} TINYTEXT);''')
		self.connection.commit()
		return True

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
			cursor = self.connection.cursor()
			cursor.execute(f"SELECT MAX(ID) FROM CS;")
			result = cursor.fetchone()
			if result is not None:
				return result[0]
		return True

	def read(self, table="", where={}, explicit=[]):
		condition, explicit = [], [self.sanitize(field) for field in explicit] if explicit else "*"
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT {' AND '.join(explicit)} FROM {table} WHERE {' AND '.join(condition)};")
		result = cursor.fetchall()
		if result is not None:
			return result
		return False

	def sanitize(self, value="", quotes = True):
		if type(value)==str and value != "NULL":
			return value.replace('\'','\'\'') if not quotes else "'" + value.replace('\'','\'\'') + "'"
		return value

	def clear(self, tables=[]):
		for table in tables:
			self.connection.executescript(f"DELETE FROM {table}; VACUUM;")
		self.connection.commit()
		return True
