"CMD Tips"
	alt+d   #type cmd, opens in that folder
	super+r #type cmd, anywhere
	ctrl+alt+p #directly open
	d:      #to switch directory
	dir     #to show directory,
	start.  #to open file exporer there
	> "for output redirect "
	2> "for error redirect"
	#add suffic to multiple
	for %a in (*) do ren "%a" "Task - %a"
	#link a specific folder to One Drive
	mklink /j "%UserProfile%\OneDrive\From Nawfal\SublimeText" "D:\Nawfal\SublimeText"
	#check if files are greater than 1 mb
	forfiles /S /C "cmd /c if @fsize GEQ 1048576 echo @path @fsize" > Size.txt

"Pip Tips"
	pip install -U pip #upgrade pip
	pip install -U PackageName #upgrade packagename
	pip list 	-o #check outdated packages
	pip list 	-u #check uptodate packages

"Sublime Tips"
	sublime.log_input(True)
	sublime.log_commands(True)
	sublime.find_resources('*.sublime-commands')
	sublime.yes_no_cancel_dialog("Do You Want To Create Input File?")
	#Try Changning word seperators in settings
	#Syntax Specific KeyBinding
	"context": [{ "key": "selector", "operator": "equal", "operand": "text.html.markdown" }],
	#Description in Snippets
	"<description>For Enumerate Loop</description>"
	#Location Specifing
	"${1:this}"
	#Sample Build
{
	"shell_cmd": "DOSBoxPortable.exe.lnk",
	"working_dir": "${file_path}",
	"selector": "source.assembly",
	"file_patterns" : "*.asm",
}
	#Sample Macro
[
	{
		"args": null,
		"command": "set_mark"
	},
	{
		"args":
		{
			"to": "line"
		},
		"command": "expand_selection"
	},
]
"Others:"
	#sort both lists according to (reverse) sorting order of first
	list1, list2 = (list(_) for _ in zip(*sorted(zip(list1,list2),reverse = True)))
	#
	reg expression : select all till second comma: ^([,]*,[^,]*)
	@njit(error_model='numpy',parallel=True,fastmath=True)
	# use isinstance fpr type check
	nasm -f win32 forwin32.asm
	link /SUBSYSTEM:WINDOWS user32.lib forwin32.obj
	nasm -f win64 forwin64.asm
	link /LARGEADDRESSAWARE:NO /SUBSYSTEM:WINDOWS user32.lib forwin64.obj
	nasm -f win64 forwin64_console.asm
	link /LARGEADDRESSAWARE:NO /ENTRY:main user32.lib kernel32.lib forwin64_console.obj

#old hostname
DESKTOP-2NT06QL
