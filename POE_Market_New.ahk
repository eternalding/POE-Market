;Reload;

~LButton & r::
reload ;
return

;+--------------------------------------------------------------------------------------------
~^C::  ;ctrl+c
index = 0
clipboard =  ; Start off empty to allow ClipWait to detect when the text has arrived.
Send ^c
ClipWait  ; Wait for the clipboard to contain text.

Run C:\POE_Market_New.exe,,Min




MMyVar := "Now acquiring infos from POE_Market..."
Tooltip ,%MMyVar%,,,

Loop
{
	NNewVar:=clipboard
	if (NNewVar != MMyVar)
		{
			break
		}
	MMyVar:=NNewVar
}




MyVar :=clipboard
StringLen, Length, MyVar
;MsgBox %Length%
;MsgBox %clipboard%
;MsgBox %MyVar%

sleep, 4500

;Display Message 

Tooltip ,%clipboard%,,,
CoordMode, Mouse, Screen   
MouseGetPos, xpos, ypos,,,1  

;Keep running until cursor moves

Loop
{
	NewVar:=clipboard
	if (NewVar != MyVar)
		{
			Tooltip ,%clipboard%,,,
		}
	IfWinNotExist, C:\POE_Market_New.exe
		{
			ToolTip
			break
		}
	MyVar:=NewVar
}
;Close Tooltip
return


