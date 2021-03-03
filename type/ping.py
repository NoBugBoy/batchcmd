import subprocess

from ssh import hostparser
from ssh.config import SSH

cmd = 'ssh-copy-id {}@{}'


def copySSHId(group):
    sshArray = hostparser.parserSSH(group)
    for ssh in sshArray:
        if ssh['isPassword']:
            print(subprocess.getstatusoutput(cmd.format(ssh['username'], ssh['value'])))
        else:
            print(ssh['host'] + '不是密码模式。不支持批量copy')


if __name__ == '__main__':
    copySSHId('web')
