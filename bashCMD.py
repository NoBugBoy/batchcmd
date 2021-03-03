import argparse
import threading

from ssh import hostparser
from ssh.config import SSH

if __name__ == '__main__':
    sshList = []
    parser = argparse.ArgumentParser()  # 首先创建一个ArgumentParser对象
    parser.add_argument('-g', required=True,
                        help='host group name')
    parser.add_argument('-i', required=False, action='store_true',
                        help='Open interactive operation')
    parser.add_argument('-c', required=True,
                        help='shell command')

    args = parser.parse_args()

    # args
    group = args.g
    sshArray = hostparser.parserSSH(group)
    if sshArray is not None:
        for ssh in sshArray:
            if ssh['isPassword']:
                if args.i:
                    sshList.append(SSH(ssh['host'], ssh['username'], ssh['value'], None, 1, group, args.c))
                else:
                    sshList.append(SSH(ssh['host'], ssh['username'], ssh['value'], None, 0, group, args.c))
            else:
                if args.i:
                    sshList.append(SSH(ssh['host'], ssh['username'], None, ssh['value'], 1, group, args.c))
                else:
                    sshList.append(SSH(ssh['host'], ssh['username'], None, ssh['value'], 0, group, args.c))
        for ssh in sshList:
            ssh.start()
        run = True
        if args.i:
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
        else:
            for ssh in sshList:
                ssh.join()