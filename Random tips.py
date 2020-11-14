class Python:
	#sort both lists according to (reverse) sorting order of first
	list1, list2 = (list(_) for _ in zip(*sorted(zip(list1,list2),reverse = True)))
	@njit(error_model='numpy',parallel=True,fastmath=True)
	# use isinstance for type check

	# reg expression : select all till second comma:
	^([,]*,[^,]*)

	class Pip:
		pip install -U pip #upgrade pip
		pip install -U PackageName #upgrade packagename
		pip list 	-o #check outdated packages
		pip list 	-u #check uptodate packages

class CommandPrompt:
	cls		# clear screen
	alt+d		# type cmd, opens in that folder
	super+r	# type cmd, anywhere
	d:			# to switch directory
	dir		# to show directory,
	start.	# to open file exporer there
	> 			# for output redirect
	2>			# for error redirect
	#add suffix to multiple
	for %a in (*) do ren "%a" "Task - %a"
	#link a specific folder to One Drive
	mklink /j "%UserProfile%\OneDrive\From Nawfal\SublimeText" "D:\Nawfal\SublimeText"
	#check if files are greater than 1 mb
	forfiles /S /C "cmd /c if @fsize GEQ 1048576 echo @path @fsize" > Size.txt

	class Nasm:
		nasm -f win32 forwin32.asm
		link /SUBSYSTEM:WINDOWS user32.lib forwin32.obj
		nasm -f win64 forwin64.asm
		link /LARGEADDRESSAWARE:NO /SUBSYSTEM:WINDOWS user32.lib forwin64.obj
		nasm -f win64 forwin64_console.asm
		link /LARGEADDRESSAWARE:NO /ENTRY:main user32.lib kernel32.lib forwin64_console.obj

class Linux:
	# for all files do a command
	for FILE in *;do unrar x $FILE; done
	# crop
	ffmpeg -i "AlignTrim.mp4" -vf "crop=300:150:450:40" AlignCrop.mp4
	# crop and convert to gif
	ffmpeg -i AlignCrop.mp4 -vf "crop=300:150:450:40;scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 Align.gif
class Git:
	# Removing a folder
	path_to_folder/ # add this to gitignore
	git rm -r --cached path_to_folder/

#old hostname
DESKTOP-2NT06QL
