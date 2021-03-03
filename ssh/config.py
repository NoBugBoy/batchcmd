import sys
import time
import paramiko
import re
import threading

from ssh import colors, hostparser

ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"


class SSH(threading.Thread):
    def __init__(self, ip, username, password, privateKey, types, group, command):
        super().__init__()
        self.setDaemon(True)
        self._types = types
        self._ip = ip
        self._client = None
        self._group = group
        self._username = username
        self._password = password
        self._privateKey = privateKey
        self._defaultCommand = command
        # 0代表未初始化完成,1代表已经就绪,2代表指令执行完毕等待处理输出
        self._status = 0
        self._data = ''
        self._output = []
        self._channel = None
        self.initCheck()

    def setDefaultCommand(self, command):
        # 仅执行一次或初始命令
        self._defaultCommand = command

    def exec(self, command):
        # 执行交互命令使用
        if self._channel is not None:
            self._defaultCommand = command
            if command == 'exit':
                self.close()
            elif self._status == 2:
                pass
            else:
                self._channel.send(command + "\n")

    def run(self):
        if self._client is None:
            print(f'{colors.red} {self._ip} >>> 连接初始化失败 {colors.clear}')
            return
        if self._types == 0:
            stdin, stdout, stderr = self._client.exec_command(self._defaultCommand)

            if stdout is None:
                self._data = f"{colors.blue} {stderr.read().decode('utf-8')} {colors.clear}"
            else:
                self._data = f"{colors.blue} {stdout.read().decode('utf-8')} {colors.clear}"
            self.print()
        elif self._types == 1:
            self._channel = channel = self._client.invoke_shell()
            if self._defaultCommand is not None:
                channel.send(self._defaultCommand + "\n")
            while True:
                stdout = self._channel.recv(1024 * 10240)
                text = stdout.decode('utf-8')
                if self._defaultCommand.strip() == 'exit':
                    print(f"{colors.yellow} group=[{self._group}] host=[{self._ip}]  bye ~ ")
                    break
                else:
                    if text.strip().endswith(self._defaultCommand):
                        continue
                    else:
                        self._data = self._data + text
                    if self._data.strip().endswith(']#'):
                        self._data = re.sub(r"\[\w+@\w+\s(/|.(.\w+/?)*)\]#", '', self._data)
                        self.print()
        else:
            pass

    def close(self):
        self._client.close()

    def runByType(self):
        pass

    def print(self):
        print(
            f"{colors.yellow} batchCMD group=[{self._group}] host=[{self._ip}] command=[{self._defaultCommand}] output => \n {colors.blue} {self._data} {colors.clear}")
        self._data = ''

    def initCheck(self):
        if re.match(ip_pattern, self._ip) and self._username is not None:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self._password is not None:
                print(f"{self._ip}  start connecting on password...")
                try:
                    client.connect(hostname=self._ip, port=22, username=self._username, password=self._password,
                                   timeout=10, )
                    self._status = 1
                except Exception as e:
                    print(f' {colors.red} {self._ip} {e} {colors.clear}')
                    return
                print(f"{colors.green} {self._ip}  connected {colors.clear}")
                self._client = client
            elif self._privateKey is not None:
                print(f"{self._ip}  start connecting on private key...")
                try:
                    client.connect(hostname=self._ip, port=22, username=self._username, pkey=self._privateKey,
                                   timeout=10)
                    self._status = 1
                except Exception as e:
                    print(f'{colors.red} {self._ip} {str(e)} {colors.clear}')
                    return
                print(f"{colors.green} {self._ip}  connected {colors.clear}")
                self._client = client


if __name__ == '__main__':
    sshList = []
    sshArray = hostparser.parserSSH('web')
    if sshArray is not None:
        for ssh in sshArray:
            if ssh['isPassword']:
                sshList.append(SSH(ssh['host'], ssh['username'], ssh['value'], None, 1, "web", 'ls'))
            else:
                sshList.append(SSH(ssh['host'], ssh['username'], None, ssh['value'], 1, "web", 'ls'))
        run = True
        for ssh in sshList:
            ssh.start()

        try:
            while run:
                command = input('\n')
                for ssh in sshList:
                    if command == '':
                        continue
                    if command == 'cc':
                        ssh.exec("\x03")
                    if command == 'exit':
                        ssh.exec(command)
                        run = False
                    else:
                        ssh.exec(command)
        except KeyboardInterrupt as e:
            pass
