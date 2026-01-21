#define MyAppName "An Optimal Samples Selection System"
#define MyAppVersion "1.0.0"
#define MyAppPublisher ""
#define MyAppExeName "OptimalSamplesSelection.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-47D7-8A9B-0C1D2E3F4A5B}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\\..\\dist-installer
OutputBaseFilename=OptimalSamplesSelectionSetup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\\..\\dist\\OptimalSamplesSelection\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
