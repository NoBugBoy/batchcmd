import configparser

from ssh import colors

cfg = configparser.ConfigParser(allow_no_value=True, )
cfg.read("sshGroup.cfg", encoding="utf-8")


def buildData(sshObj, host, username, isPassword, value):
    sshObj.append(
        {
            "host": host,
            "username": username,
            "isPassword": isPassword,
            "value": value
        }
    )


def parserSSH(group):
    try:
        items = cfg.items(group)
        sshObj = []
        for item in items:
            ssh = item[0].split(' ')
            if len(ssh) == 3:
                if ssh[1] == '-p':
                    # 密码模式
                    buildData(sshObj, ssh[0], 'root', True, ssh[2])
                else:
                    # 私钥模式
                    buildData(sshObj, ssh[0], 'root', False, ssh[2])
            elif len(ssh) == 5:
                if ssh[3] == '-p':
                    # 密码模式
                    buildData(sshObj, ssh[0], ssh[2], True, ssh[4])
                else:
                    # 私钥模式
                    buildData(sshObj, ssh[0], ssh[2], False, ssh[4])
            else:
                print('格式有误 请检查sshGroup.cfg')
        return sshObj
    except configparser.NoSectionError as e:
        print(f'{colors.red} 未发现名为{group}的分组.. {colors.clear}')
