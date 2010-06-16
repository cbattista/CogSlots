!define PRODUCT_NAME "CogSlots"
!define PRODUCT_VERSION "0.1"
!define PRODUCT_PUBLISHER "Jobe Software"
;!define PRODUCT_WEB_SITE "http://jehiah.com/projects"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "setup.exe"
InstallDir "$PROGRAMFILES\CogSlots"

Section "Main" SEC01
	SetOutPath "$INSTDIR"
	SetOverwrite ifnewer
	;File /r "src"
	File /r "pkgs"
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

;Section "Python Setuptools" SEC03
;	ExecWait '"$INSTDIR\pkgs\setuptools-0.6c11.win32-py2.6"'

;SectionEnd

Section "wxPython" SEC04	
	;Use easy_install for python package deps
	!system '$INSTDIR\pkgs\wxPython2.8-win32-unicode-2.8.11.0-py26.exe' > 0
SectionEnd


