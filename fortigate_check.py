########################################################
# Fortigate30E~ or Fortigate60E~ get state
########################################################


#================================================
# import module
#================================================
from Exscript.protocols import SSH2
from Exscript import Account
import datetime
import time
import getpass
import sys
import string

#================================================
# prompt
#================================================
print '='*45
print '\033[1;32m' + 'Fortigate Check script' + '\033[0;39m'
print '='*45
Day         = datetime.date.today()
DATE        = Day.strftime("%Y%m%d")
UserName    = 'admin'
HNAME       = raw_input('Fortigate\'s Hostname: ')
IPv4        = raw_input('IPv4 Address: ')
VPN         = raw_input('VPN (y/n): ')
PASS        = getpass.getpass('Password: ')

#================================================
# Open Write File
#================================================
file = open('/root/ftg_tmp.txt', 'w')
cnf = open('/root/ftg_conf.txt', 'w')

#================================================
# mk_config
#================================================
cnf.write('IPADDRESS=\"'+IPv4+'\"\n')
cnf.write('HOST=\"'+HNAME+'\"')
cnf.close()

#================================================
# Connect by SSH
#================================================
session = SSH2()
session.connect(IPv4)

#================================================
# login to Fortigate
#================================================
session.login(Account(name=UserName, password=PASS))

#================================================
# command
#================================================
#------------------------------------------------
# std_out
#------------------------------------------------
print '\033[35m' + 'Command Sending to '+HNAME+'...' + '\033[0;39m'
session.execute('config system console')
session.execute('set output standard')
session.execute('end')

#------------------------------------------------
# Command List
#------------------------------------------------
Command =[  'get system status',
            'get system fortiguard | grep license',
            'get system interface physical',
            'show firewall policy',
            'show spamfilter profile',
            'show spamfilter bwl',
            'show antivirus profile default',
            'show firewall address',
            'diagnose sys ha status',
            'show system ha',
            'get system ha | grep mode',
            'show firewall vip',
            'show system admin',
            'get user local',
            'show user group',
            'show system accprofile']

#------------------------------------------------
# exe command result write to tmp file
#------------------------------------------------
for exe_command in Command:
    session.execute(exe_command)
    #file.write(session.response.encode())
    file.write(session.response.encode('utf8'))
    time.sleep(0.1)

#------------------------------------------------
# Check VPN setting
#------------------------------------------------
if VPN == 'y':
    session.execute('show vpn ssl settings')
    file.write(session.response.encode())
    session.execute('show vpn ssl web portal')
    file.write(session.response.encode())
    time.sleep(0.1)
    session.execute('show vpn ipsec phase1-interface')
    file.write(session.response.encode())
    session.execute('show vpn ipsec phase2-interface')
    file.write(session.response.encode())

#------------------------------------------------
# Save the config file
#------------------------------------------------
print '\033[35m' + 'Now saving to xxx.xxx.xxx.xxx ...' + '\033[0;39m'
session.execute('execute backup config tftp fortigate_config/'+HNAME+'_'+IPv4+'_'+DATE+'.cfg xxx.xxx.xxx.xxx')
print '\033[35m' + 'Save had finished !!' + '\033[0;39m'

#------------------------------------------------
# std_out more
#------------------------------------------------
session.execute('config system console')
session.execute('set output more')
session.execute('end')

#------------------------------------------------
# Fin
#------------------------------------------------
file.close()
print '\033[35m' + 'Finish! Result data wrote to tmpfile' + '\033[0;39m'

#================================================
# Disconnect by SSH
#================================================
if session:
    session.send('exit')
    session.close()
else:
    raise AttributeError('Can not find a lived session')
