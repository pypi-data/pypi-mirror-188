#include <Constants.au3>
;
; AutoIt Version: 3.0
; Language:       English

_Example()
Exit
; Finished!

Func _Example()

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("de 10 u{ENTER}")
	Sleep(30000)

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("set_load 120{ENTER}")
	Sleep(3000)

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("dc 5{ENTER}")
	Sleep(3000)

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("de 3 u{ENTER}")
	Sleep(30000)

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("dc 1{ENTER}")
	Sleep(30000)

	WinActivate("Terminal")
	WinWaitActive("Terminal")
	Send("set_load 0{ENTER}")
	Sleep(1000)

EndFunc   ;==>_Example