import winreg

path_32 = r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
hkey = winreg.HKEY_LOCAL_MACHINE

with winreg.OpenKey(hkey, path_32) as main_key32:
    with open('soft32.txt', 'w', encoding='utf-8') as outstream:
        outstream.write('{0:64} {1:32}\n\n'.format('Name', 'Version'))
        for i in range(1024):
            try:
                now_key = (winreg.EnumKey(main_key32, i))
            except:
                break
            # print(now_key)
            display_name = ''
            display_version = ''
            with winreg.OpenKey(hkey, path_32 + '\\{}'.format(now_key)) as handle32:
                for j in range(64):
                    try:
                        value = winreg.EnumValue(handle32, j)
                        if value[0] == 'DisplayName':
                            display_name = value[1]
                        if value[0] == 'DisplayVersion':
                            display_version = value[1]
                    except:
                        break
            if (display_name):
                outstream.write('{0:64} {1:32}\n'.format(display_name, display_version))
