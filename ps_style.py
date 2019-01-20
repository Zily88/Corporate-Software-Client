import subprocess

proc = subprocess.Popen(['powershell', 'chcp 65001 ; '  # Стандартные повершелл запросы + ms store
                        'Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'
                        ' | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize ;'
                        ' Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* '
                        '| Select-Object DisplayName, DisplayVersion, Publisher, Size, InstallDate | Format-Table -AutoSize ;'
                        ' Get-AppxPackage | Select Name, PackageFullName | Format-Table -AutoSize'], stdout=subprocess.PIPE)
data = proc.communicate()
data = data[0].decode('utf-8')
data = data.splitlines()
with open('power_shell.txt', 'w', encoding='utf-8') as file:
    for line in data:
        file.write(line + '\n')
