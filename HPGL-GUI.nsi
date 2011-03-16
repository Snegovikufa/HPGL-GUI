;NSIS Modern User Interface
;Welcome/Finish Page Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "HPGL-GUI"
  OutFile "HPGL-GUI_Installer.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\HPGL-GUI"


  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "LICENSE"
  ;!insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\HPGL-GUI"
  CreateShortCut "$SMPROGRAMS\HPGL-GUI\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\HPGL-GUI\HPGL-GUI.lnk" "$INSTDIR\hpgl-gui.exe" "" "$INSTDIR\hpgl-gui.exe" 0
  
SectionEnd


Section ""

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  File /r "HPGL-GUI-builded\*.*"

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDummy ${LANG_ENGLISH} "A test section."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDummy} $(DESC_SecDummy)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\*.*"
  Delete "$SMPROGRAMS\HPGL-GUI\*.*"
  RMDir /r "$SMPROGRAMS\HPGL-GUI"

  RMDir /r "$INSTDIR"

SectionEnd
