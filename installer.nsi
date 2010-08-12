!define PRODUCT_NAME "CogSlots"
!define PRODUCT_VERSION "0.1"
!define PRODUCT_PUBLISHER "Jobe Microsystems"
;!define PRODUCT_WEB_SITE ""

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "setup.exe"
InstallDir "$PROGRAMFILES\CogSlots"

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
	File "README"
	File "Settings.py"
	File "SlotReels.py"
	File "cfg.py"
	File "commongui.py"
	File "gameplay.py"
	File "introtext.html"
	File "setupgui.py"
	File "subjectinfo.py"
	File "brain_icon.ico"
	
	File /r "images"
	File /r "settings"
	File /r "pkgs"
	
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

Section "wxPython" SEC04
	;Use easy_install for python package deps
	ExecWait '$INSTDIR\pkgs\wxPython2.8-win32-unicode-2.8.11.0-py26.exe'
SectionEnd

Section "PyOpenGL" SEC05
	ExecWait '$INSTDIR\pkgs\PyOpenGL-3.0.1.win32.exe'
SectionEnd

Section "Finalize" SEC06	
	;Create useful shortcuts
	CreateDirectory "$SMPROGRAMS\CogSlots"
	CreateShortcut "$SMPROGRAMS\CogSlots\Game.lnk" "python" "$INSTDIR\gameplay.py"
	CreateShortcut "$SMPROGRAMS\CogSlots\SetupExperiment.lnk" "python" "$INSTDIR\setupgui.py"
	CreateShortcut "$SMPROGRAMS\CogSlots\README.lnk" "notepad" "$INSTDIR\README"
	CreateSHortcut "$SMPROGRAMS\CogSlots\uninstall.lnk" "$INSTDIR\uninstall.exe"	
SectionEnd

Section "Uninstall" SEC07
	RMDir /r $INSTDIR
	RMDir /r "$SMPROGRAMS\CogSlots"
SectionEnd


