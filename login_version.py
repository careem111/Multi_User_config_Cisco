import paramiko
import time
import os
import traceback


class GetConfig(object):
    # class variables
    remote_conn_pre = ''
    remote_conn = ''
    hostname = ''
    ios_version = ''

    def __init__(self, ip):

        self.ip = ip

    def login(self):

        login_credential = [('username1', 'password1', 'secret1'), ('username2', 'password2', 'secret2'),
                                ('username3', 'password3', 'secret3')]
        attempts = 0
        # print(self.ip)
        while attempts < 4:
            for username, password in login_credential:
                attempts += 1

                self.remote_conn_pre = paramiko.SSHClient()
                self.remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    self.remote_conn_pre.connect(self.ip, username=username, password=password, timeout=5,
                                                 allow_agent=False, look_for_keys=False)

                except:
                    attempts += 1
                    print(self.ip, attempts)
                    continue

                self.remote_conn = self.remote_conn_pre.invoke_shell()
                time.sleep(3)

                print(self.hostname)

                if '>' in self.hostname:
                    self.remote_conn.send('enable\n')
                    time.sleep(2)
                    output = self.remote_conn.recv(1048576)
                    self.remote_conn.send(password + '\n')
                    time.sleep(2)
                    output = self.remote_conn.recv(1048576)

                self.remote_conn.send('terminal length 0\n')
                time.sleep(5)
                output = self.remote_conn.recv(1048576)

                if attempts == 12:
                    print("$$$$$$$$$$$$$$$$$$$$$$$")
                    print("\nError in " + self.ip + "\n")
                    print(traceback.format_exc() + "\n")
                    print("$$$$$$$$$$$$$$$$$$$$$$$")
                    os.chdir('/home/mhariry/fo-bgp-mon/')
                    output = open('unreachable-dev-' + time.strftime("%Y%m%d") + '.csv', 'a')
                    output.write(self.ip + '\n')
                    output.close()

                break
            break

    def version(self):
        self.remote_conn.send('sh ver\n')
        time.sleep(5)
        output = self.remote_conn.recv(1048576)
        doutput = output.decode('utf-8')
        if 'IOS-XE' in doutput:

            self.ios_version = 'IOS-XE'
        elif 'NX-OS' in doutput:

            self.ios_version = 'NX-OS'
        else:

            self.ios_version = 'IOS'


