class Console:
	sublime.log_input(True)
	sublime.log_commands(True)
	sublime.find_resources('*.sublime-commands')
	sublime.yes_no_cancel_dialog("Do You Want To Create Input File?")

class KeyBindings:
	#Try Changing word separators in settings
	#Syntax Specific KeyBinding
	"context": [{ "key": "selector", "operator": "equal", "operand": "text.html.markdown" }],

class Snippets:
	#Description in Snippets
	"<description>For Enumerate Loop</description>"
	#Location Specifying
	"${1:this}"

class Builds:
{
	"shell_cmd": "DOSBoxPortable.exe.lnk",
	"working_dir": "${file_path}",
	"selector": "source.assembly",
	"file_patterns" : "*.asm",
}
class Macros:
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
