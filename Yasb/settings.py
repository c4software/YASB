class Settings():
	_default_values = 	{"site_title":"", 
						"author":"",
						"url":"",
						"input":"./source/",
						"output":"./output/",
						"plugin_folder":"plugins",
						"plugins":[],
						"theme":"./",
						"static":"",
						"diff_build":False,
						"diff_build_db":".diff_build_db",
						"lastbuild_file":".lastbuild",
						"title_as_name":False
						}

	values = {}
	def __init__(self, input_val):
		self.values = dict(self._default_values.items() + input_val.items())

	def get(self, key, default=""):
		if key in self.values:
			return self.values[key]
		else:
			return default
