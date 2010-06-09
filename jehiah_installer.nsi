
!define PRODUCT_NAME "Jehiah base developer install"
!define PRODUCT_VERSION "0.1"
!define PRODUCT_PUBLISHER "Jehiah"
!define PRODUCT_WEB_SITE "http://jehiah.com/projects"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "setup.exe"
InstallDir "$PROGRAMFILES\JEHIAH\base_python_install"

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r "src"
  File /r "pkgs"
SectionEnd

Section "Python" SEC02
  ExecWait 'msiexec /package "$INSTDIR\pkgs\python-2.4.3.msi" /quiet '
  ReadRegStr $0 HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "path"
  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "path" "$0;c:\python24"
SectionEnd

Section "Mysql" SEC03
  ExecWait 'msiexec /package "$INSTDIR\pkgs\mysql-essential-5.0.22-win32.msi" /quiet'
SectionEnd

Section "PyWin32" SEC04
  ; this is not a "quiet" install
  ExecWait '$INSTDIR\pkgs\pywin32-208.win32-py2.4.exe'
SectionEnd

Section "Mysqld-python" SEC05
  ; this is not a "quiet" install
  ExecWait '$INSTDIR\pkgs\MySQL-python.exe-1.2.0.win32-py2.4.exe'
SectionEnd

Section "Webware" SEC06
  ; the "\n" is because it prompts for a password
  ExecWait 'c:\python2.4\python "$INSTDIR\src\Webware-0.9.1\install.py" < "\n"'
SectionEnd