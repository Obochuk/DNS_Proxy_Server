To start the dns proxy server use command like this:
    python twistd.py -y DNSProxy.tac
Server starts in the localhost and in the standard port(127.0.0.1:53)
To configure server use file config.ini, and use the same rules that used in the start. If there are some error, server may
 crash)

 Versions: python 2.7, twisted 12.0

 May require environment variable PATH set to the python folder and python/Scripts folder