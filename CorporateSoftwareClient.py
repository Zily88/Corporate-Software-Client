from get_soft_method import Method, PowerShellMethod, WinregMethod, WmiMethod
import abc
import platform
import os
import json
import requests
URL = 'xxx.xxx.xxx.xxx'
PORT = 'xxxx'

class Client(metaclass=abc.ABCMeta):

    methods = []
    soft = []
    info = {}
    os = {}
    machine_name = ''
    username = ''

    def get_soft(self):
        for method in self.methods:
            self.soft.extend(method.get_soft_list())

    @abc.abstractmethod
    def send_json_info(self):
        pass

    @abc.abstractmethod
    def get_computer_info(self):
        pass

class ClientWin10x64(Client):

    def __init__(self):
        self.methods.append(WinregMethod())
        self.methods.append(WmiMethod())
        self.methods.append(PowerShellMethod())
        self.get_computer_info()
        # Можеть быть через super().__init__() если наберётся побольше общих методов...
        self.get_soft()

    def get_computer_info(self):
        self.os['type'] = platform.uname().system
        self.os['version'] = platform.uname().version
        self.machine_name = platform.uname().node
        self.username = os.getlogin()

    def send_json_info(self):
        json_for_send = {'OS': self.os, 'machine_name': self.machine_name, 'username': self.username, 'soft': self.soft}
        json_for_send = json.dumps(json_for_send)
        # Это я не протестил джангу не поднял пока...
        r = requests.post('{}:{}'.format(URL, PORT), json=json_for_send)


# Ну и в идеале это должно работать...
# ClientWin10x64().send_json_info()



