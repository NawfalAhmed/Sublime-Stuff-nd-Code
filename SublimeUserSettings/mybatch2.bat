((tasklist | find /i "dosbox.exe" > nul && taskkill /f /im dosbox.exe > nul) & start /min D:\\Nawfal\\SublimeText\\Assembly\\DOSBoxPortable\\App\\Dosbox\\Dosbox -c "mount D ${file_path}" -c D: -c "C:nasm ${file_name} -o ${file_base_name}.com -l ${file_base_name}.lst -E error.txt " -c exit ) > nul
:repeat
tasklist | find /i "dosbox.exe" > nul && goto :repeat || type error.txt && ping 127.0.0.1 -n 8 > nul
