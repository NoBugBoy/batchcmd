import re

if __name__ == '__main__':
    str = re.sub(r'\[\w+@\w+\s(w+|~|.)\]#', '', """Last login: Tue Mar  2 21:04:15 2021 from 172.16.3.1
anaconda-ks.cfg  flannel.tar                             kube-flannel.yml
flanneld         flannel-v0.13.1-rc1-linux-amd64.tar.gz  mk-docker-opts.sh
flannel.img      init-config.yaml                        README.md
[root@node1 ~]# 
Last login: Tue Mar  2 21:04:15 2021 from 172.16.3.1
anaconda-ks.cfg  flannel.tar                             kube-flannel.yml
flanneld         flannel-v0.13.1-rc1-linux-amd64.tar.gz  mk-docker-opts.sh
flannel.img      init-config.yaml                        README.md
[root@node1 ~]# 
Last login: Tue Mar  2 21:03:52 2021 from 172.16.3.1
abc.txt  anaconda-ks.cfg  flannel.img
[root@node2 ~]# 
Last login: Tue Mar  2 21:03:52 2021 from 172.16.3.1
abc.txt  anaconda-ks.cfg  flannel.img
[root@node2 ~]# """)
    print(str)