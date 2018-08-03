import netmiko
import time
from netmiko.ssh_exception import NetMikoTimeoutException


class GetConfig(object):
    # class variables

    connection = ''
    hostname = ''
    ios_version = ''
    connect_status = False

    def __init__(self, ip):

        self.ip = ip

    def login(self):

            ''' function to login to the cisco device'''

            netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                              netmiko.ssh_exception.NetMikoAuthenticationException)
    
            # multiple user credential
            login_Credential = [('username1', 'password1', 'secret1'), ('username2', 'password2', 'secret2'),
                                ('username3', 'password3', 'secret3')]
            attempts = 0
    
            try:
                while attempts < 4:
                    print('-'*79)
                    print('connecting to device', self.ip)
                    for username, password, secret in login_Credential:
                        attempts += 1
                        try:
                            self.connection = netmiko.ConnectHandler(ip,  port=22, device_type='cisco_ios',
                                                                username=username, password=password, secret=secret)
                            self.connection.enable()
                            time.sleep(1)
                            hostname = self.connection.find_prompt() + '\n'
                            print(hostname)  # printing hostname
                           
                            if '#' in hostname:
                                    self.connect_status = True
                                    self.connection.send_command('\n')
                            
                                    self.connection.send_command('terminal length 0' + '\n' )
                        except:
                            print('check the network status')
                            if attempts > 3:
                                print('check the credentials')
                            continue

                        self.connection.clear_buffer()
         
                        self.connection.disconnect()

                        break
                    break

            except netmiko_exceptions as e:
                print('fail to', ip, e)
                print(ip)
                text_file = open('FailedDevices', 'a')
                text_file.write(self.ip+'\n')
                text_file.close()


    def version(self):

        ''' function to check the IOS version in cisco devices'''
        if self.connect_status == True:

            output = self.connection.send_command('sh ver' + '\n')
            time.sleep(5)
            doutput = output.decode('utf-8')
            if 'IOS-XE' in doutput:
                self.ios_version = 'IOS-XE'
            elif 'NX-OS' in doutput:
                self.ios_version = 'NX-OS'
            else:
                self.ios_version = 'IOS'
