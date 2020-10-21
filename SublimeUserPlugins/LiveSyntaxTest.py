# import sublime
# import sublime_plugin

# class LiveSyntaxTest(sublime_plugin.ViewEventListener):
# 	def __init__(self, *args, **kw):
# 		super().__init__(*args, **kw)
# 		self.syntax_running = 0
# 		self.mode = "use32"

# 	@classmethod
# 	def is_applicable(self,settings):
# 		return "Assembly x86.tmLanguage" in settings.get("syntax")
# 	def on_activated(self):
# 		view = self.view
# 		self.mode = view.substr(view.line(0))
# 	def on_text_command(self,command_name,args):
# 		view = self.view

# 		def show_error(filepath2,line):
# 			errorfile = open(filepath2,"r")
# 			errortext = errorfile.read()[len(filepath2)+4:]
# 			# length = len(filepath2)+4
# 			# errortext = [eline[length:] for eline in errorfile.readlines()]
# 			# errortext = "\n".join(errortext)
# 			errorfile.close()

# 			self.syntax_running -=1

# 			view.erase_phantoms("Error Code")
# 			if errortext.isspace() or not errortext or "does not support external" in errottext:
# 				return
# 			errortext = "<style> body { background-color: color(var(--redish) blend(var(--background) 30%));} error { color: #f1f1f1;padding: 0.4rem 0.2 0.4rem 3rem } </style> <error> " + errortext + " </error>"
# 			view.add_phantom("Error Code", line, errortext, sublime.LAYOUT_BLOCK)

# 		def check_for_errors(filepath,filepath2,line):
# 			view.window().run_command("run_cmd",{"cmd":"nasm \"" +filepath+"\" -Z \"" +filepath2+"\"","show_panel": False})
# 			sublime.set_timeout_async(lambda: show_error(filepath2,line),250)

# 		def run_test():
# 			filepath = "C:\\Users\\nawfall\\AppData\\Roaming\\Sublime Text 3\\Packages\\UserPlugins\\nasmtest.asm"
# 			filepath2 = "C:\\Users\\nawfall\\AppData\\Roaming\\Sublime Text 3\\Packages\\UserPlugins\\nasmtest.txt"
# 			symbols = [symbol[1].strip("\t ").replace("\t","") for symbol in view.symbols() if not symbol[1].isspace()]
# 			labels, externs = [], []
# 			for symbol in symbols:
# 				if ":" == symbol[-1]:
# 					labels.append(symbol)
# 				elif symbol[0].isupper() and symbol not in externs:
# 					externs.append(symbol)
# 			filetext = self.mode + "\n"
# 			for extern in externs:
# 				filetext += "extern " + extern + "\n"
# 			filetext += "\n".join(labels)
# 			line = view.line(view.sel()[0].a)
# 			filetext += "\n"+ (view.substr(line))

# 			testfile = open(filepath,"w+")
# 			testfile.write(filetext)
# 			testfile.close()

# 			if self.syntax_running < 1:
# 				self.syntax_running+=1
# 				sublime.set_timeout_async(lambda: check_for_errors(filepath,filepath2,line),20)

# 		if "by" in args:
# 			if args["by"] == "lines":
# 				run_test()

# 		if args == {'characters': '\n'} and command_name == "insert":
# 			run_test()
