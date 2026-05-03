---
name: install-chrome-windows
description: Install Google Chrome on Windows from Codex or PowerShell. Use when the user asks to install Chrome, fix a failed Chrome installation, work around winget download failures, handle dl.google.com TLS/EOF/ECONNRESET errors, or install Chrome from a downloaded MSI with UAC/admin elevation.
---

# Install Chrome on Windows

## Workflow

1. Check whether Chrome is already installed:

```powershell
Get-Command chrome,chrome.exe -ErrorAction SilentlyContinue | Select-Object Name,Source
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -like '*Google Chrome*' } |
  Select-Object DisplayName,DisplayVersion,InstallLocation,Publisher
```

2. Try the normal package-manager path first when `winget` is available:

```powershell
winget install --id Google.Chrome --source winget --accept-package-agreements --accept-source-agreements --silent
```

If this fails with `InternetOpenUrl() failed`, `0x80072efd`, TLS authentication errors, unexpected EOF, or resets from `dl.google.com`, treat it as a download-path problem and continue with the fallback CDN.

3. Download the offline enterprise MSI from Google's alternate CDN:

```powershell
node -e "const fs=require('fs'); const https=require('https'); const url='https://edgedl.me.gvt1.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi'; const out='D:/testproject/GoogleChromeStandaloneEnterprise64.msi'; const file=fs.createWriteStream(out); file.on('error',e=>{console.error(e); process.exit(1);}); https.get(url,res=>{ if(res.statusCode!==200){ console.error('status',res.statusCode); process.exit(1);} res.pipe(file); file.on('finish',()=>file.close(()=>console.log('downloaded '+out))); }).on('error',e=>{console.error(e); process.exit(1);});"
```

Adjust `out` to a writable workspace path. Avoid `C:\tmp` unless you have confirmed it is writable; Windows ACLs may deny writes even when the Codex sandbox lists it as writable.

4. Confirm the MSI looks valid:

```powershell
Get-Item D:\testproject\GoogleChromeStandaloneEnterprise64.msi | Select-Object FullName,Length,LastWriteTime
Format-Hex -Path D:\testproject\GoogleChromeStandaloneEnterprise64.msi -Count 16
```

A real MSI begins with `D0 CF 11 E0 A1 B1 1A E1` and is usually large, roughly 100 MB or more.

5. Install with MSI logging:

```powershell
msiexec.exe /i D:\testproject\GoogleChromeStandaloneEnterprise64.msi /qn /norestart /L*v D:\testproject\chrome_install.log
```

If the log shows `Error 1925` or "You do not have sufficient privileges to complete this installation for all users", rerun via UAC elevation:

```powershell
Start-Process msiexec.exe -ArgumentList '/i "D:\testproject\GoogleChromeStandaloneEnterprise64.msi" /qn /norestart /L*v "D:\testproject\chrome_install_admin.log"' -Verb RunAs -Wait
```

Ask the user to approve the Windows UAC prompt when it appears.

6. Verify installation:

```powershell
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
  Where-Object { $_.DisplayName -like '*Google Chrome*' } |
  Select-Object DisplayName,DisplayVersion,InstallLocation,Publisher

Get-ChildItem 'C:\Program Files','C:\Program Files (x86)',"$env:LOCALAPPDATA" -Recurse -Filter chrome.exe -ErrorAction SilentlyContinue |
  Select-Object -First 20 FullName,Length

(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo |
  Select-Object ProductVersion,FileVersion
```

Prefer file `VersionInfo` for a clean version check. Running `chrome.exe --version` can emit a Crashpad access-denied warning even when Chrome installed successfully.

## Notes

- Use escalation for commands that install system software or trigger UAC.
- Keep installer logs in the workspace until verification is complete; they are the fastest way to distinguish network, privilege, and installer failures.
- The working fallback that succeeded was `https://edgedl.me.gvt1.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi`.
