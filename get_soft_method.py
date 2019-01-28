import abc
import wmi
import winreg
import subprocess


class Method(metaclass=abc.ABCMeta):
    soft_list = []

    @abc.abstractmethod
    def get_soft_list(self):
        """
        :return: list of a dicts
        """
        return self.soft_list


class WmiMethod(Method):

    def get_soft_list(self):
        for product in wmi.WMI().Win32_Product():
            self.soft_list.append({'DisplayName': '{}'.format(product.Caption), 'DisplayVersion':
                                  '{}'.format(product.Version)})
        return self.soft_list


# print(WmiMethod().get_soft_list())


class WinregMethod(Method):

    def __init__(self, hkey=None, subkey=None, *args):
        if hkey:
            self.hkey = hkey
        else:
            self.hkey = winreg.HKEY_LOCAL_MACHINE
        if subkey:
            self.subkey = subkey
        else:
            self.subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        if args:
            self.args = args
        else:
            self.args = ['DisplayName', 'DisplayVersion']

    def regestry_walk(self, key, *args):
        with winreg.OpenKey(key, None) as key:
            inside_keys_length = winreg.QueryInfoKey(key)[0]
            if inside_keys_length:
                for i in range(inside_keys_length):
                    sub_key = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, sub_key) as new_key:
                        self.regestry_walk(new_key, *args)
            else:
                self.soft = {}
                for arg in args:
                    try:
                        self.soft[arg] = winreg.QueryValueEx(key, arg)[0]
                    except FileNotFoundError:
                        pass
                if self.soft:
                    self.soft_list.append(self.soft)

    def get_soft_list(self):
        with winreg.OpenKey(self.hkey, self.subkey) as win_key:
            self.regestry_walk(win_key, *self.args)
        return self.soft_list

# print(WinregMethod().get_soft_list())

class PowerShellMethod(Method):

    def __init__(self, request=None):
        self.requests = []
        if request:
            self.requests.append(request)
        else:
            self.requests.append({'DisplayName': 'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\'
                                                'CurrentVersion\\Uninstall\\*' 
                                                ' | Select-Object DisplayName'})
            self.requests.append({'DisplayVersion': 'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\'
                                                 'CurrentVersion\\Uninstall\\*' 
                                                 ' | Select-Object DisplayVersion'})

    def my_zip(self, some_list):
        result_list = []
        _ = 0
        if len(some_list) > 1:
            result = list(zip(*some_list))
            for some_tuple in result:
                new_dict = {}
                for some_dict in some_tuple:
                    for key, value in some_dict.items():
                        new_dict[key] = value
                result_list.append(new_dict)
        else:
            return some_list
        return result_list

    def get_soft_list(self):
        result_list = []
        for request in self.requests:
            proc = subprocess.Popen(['powershell', 'chcp 65001 ; {}'.format(list(request.values())[0])],
                                    stdout=subprocess.PIPE)
            data = proc.communicate()
            data = data[0].decode('utf-8')
            data = data.splitlines()
            new_data = []
            for string in data[4:]:
                if not string.isspace():
                    new_data.append({list(request.keys())[0]: string.strip()})
            result_list.append(new_data)
        result = self.my_zip(result_list)
        return result

# print(PowerShellMethod().get_soft_list())