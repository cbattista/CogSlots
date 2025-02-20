!define PRODUCT_NAME "CogSlots"
!define PRODUCT_VERSION "0.8"
!define PRODUCT_PUBLISHER "Jobe Microsystems"
!define PRODUCT_WEB_SITE "www.github.com/cbattista/cogslots"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "installCogSlots0.8.exe"
InstallDir "$PROGRAMFILES\CogSlots"

Function "GetMyDocs"
  ReadRegStr $0 HKCU \
             "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" \
             Personal
FunctionEnd

;Disallow concurrent installers
Function .onInit
	System::Call 'kernel32::CreateMutexA(i 0, i 0, t "CogSlotsMutex") i .r1 ?e'
	Pop $R0
	
	StrCmp $R0 0 +3
		MessageBox MB_OK|MB_ICONEXCLAMATION "The installer is already running."
		Abort
FunctionEnd

Section "Main" SEC01
	SetOutPath "$INSTDIR"
	SetOverwrite ifnewer
	
	;List of source files to copy
	File "CogSub.py"
	File "Settings.py"
	File "SlotReels.py"
	File "cfg.py"
	File "commongui.py"
	File "gameplay.py"
	File "introtext.html"
	File "setupgui.py"
	File "subjectinfo.py"
	File "Shuffler.py"
	File "brain_icon.ico"
	File /r "images"
	File /r "pkgs"
	
	FileOpen $9 docpath.txt w ;Opens a Empty File an fills it
	Call "GetMyDocs"
	FileWrite $9 $0
	FileClose $9 ;Closes the filled file
  
	CreateDirectory "$0\CogSlots"
	SetOutPath "$0\CogSlots\"
	File /r "settings"
	File /r "images"
	File "introtext.html"
	
	# create the uninstaller
    writeUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Python" SEC02
	;Install python
	ExecWait 'msiexec /package "$INSTDIR\pkgs\python-2.6.5.msi" /quiet '
	
	;Make sure that python is in the path so easy_install will work later
	ReadRegStr $0 HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "path"
	;This will append the strings, how to find them and change if necessary??
	WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "path" \
	"$0;c:\python26;c:\python26\Scripts"
SectionEnd

Section "Python Setuptools" SEC03
	ExecWait '$INSTDIR\pkgs\setuptools-0.6c11.win32-py2.6'
SectionEnd

Section "vcredist" SEC04
	ExecWait '$INSTDIR\pkgs\vcredist_x86.exe'
SectionEnd

Section "wxPython" SEC05
	;Use easy_install for python package deps
	ExecWait '$INSTDIR\pkgs\wxPython2.8-win32-unicode-2.8.11.0-py26.exe'
SectionEnd

Section "PyOpenGL" SEC06
	ExecWait '$INSTDIR\pkgs\PyOpenGL-3.0.1.win32.exe'
SectionEnd

Section "Finalize" SEC07	
	;Create useful shortcuts
	CreateDirectory "$SMPROGRAMS\CogSlots"
	CreateShortcut "$SMPROGRAMS\CogSlots\Game.lnk" "$INSTDIR\gameplay.py"
	CreateShortcut "$SMPROGRAMS\CogSlots\SetupExperiment.lnk" "$INSTDIR\setupgui.py"
	CreateShortcut "$SMPROGRAMS\CogSlots\README.lnk" "notepad" "$INSTDIR\README"
	CreateShortcut "$SMPROGRAMS\CogSlots\uninstall.lnk" "$INSTDIR\uninstall.exe"	
		
SectionEnd

Section "Uninstall" SEC08
	RMDir /r $INSTDIR
	Delete $SMPROGRAMS\CogSlots\Game.lnk
	Delete $SMPROGRAMS\CogSlots\SetupExperiment.lnk
	Delete $SMPROGRAMS\CogSlots\README.lnk
	Delete $SMPROGRAMS\CogSlots\uninstall.lnk
	RMDir /r "$SMPROGRAMS\CogSlots"
	Delete $SMPROGRAMS\CogSlots

	
SectionEnd


