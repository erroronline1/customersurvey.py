# -*- coding: utf-8 -*-

from kivy import platform
from pathlib import Path
import os
import shutil
#if platform=="android":
#	from android.permissions import Permission, request_permissions, check_permission
#	from android.storage import app_storage_path
#	from androidstorage4kivy import SharedStorage

class WinShared():
	#mimics androidstorage4kivy SharedStorage to just have one super handling method for files
	def copy_to_shared(self, private_file, collection = None, filepath = None):
		shutil.copyfile(private_file, filepath)
		pass #returns shared_file or None

	def copy_from_shared(self, shared_file):
		pass #returns private_file or None

	def delete_shared(self, shared_file):
		pass #returns True if deleted, else False

class platform_handler():
	window_size = (400, 666)
	app_dir = os.path.dirname(__file__)
	shared_dir = os.path.join(str(Path.home()), "Documents")
	file = WinShared()

	def __init__(self):
		if platform=="android":
			from android.permissions import Permission, request_permissions, check_permission
			from android.storage import app_storage_path
			from androidstorage4kivy import SharedStorage
			perms = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
			def check_permissions(perms):
				for perm in perms:
					if check_permission(perm) != True:
						return False
				return True
			if check_permissions(perms)!= True:
				request_permissions(perms)	# get android permissions     
				#exit()						# app has to be restarted; permissions will work on 2nd start		
			
			self.window_size = None
			self.app_dir = app_storage_path()
			self.shared_dir = None
			self.file = SharedStorage()
	
	def fileExport(self, name, raw_content):
		try:
			temp_file=os.path.join(self.app_dir, name)
			with open(temp_file, 'w', newline='') as tfile:
				tfile.write(raw_content)
			self.file.copy_to_shared(temp_file, collection = None, filepath = name if not self.shared_dir else os.path.join(self.shared_dir, name))
			os.remove(temp_file)
			return {"success": True, "return": name}
		except Exception as e:
			return {"success": False, "return": e}