import re
import time


from login_version import GetConfig


class BgpStatus(GetConfig):

    def bgp_status(self):

        ''' Funtion to check the BGP status'''

        self.remote_conn.send('show ip bgp neighbors | i BGP neighbor|BGP state\n')
        time.sleep(5)

        output = self.remote_conn.recv(1048576)
        doutput = output.decode('utf-8')

        print(self.ios_version) # display the IOS version

        bgp_file = open('bgp_status.txt','a+')

        bgp_file.write(doutput)
        bgp_file.close()

class OspfInt(GetConfig):


    def ospf_int_brief(self):        

        ''' Function to filter the ospf interface with 'DOWN' status'''

        self.remote_conn.send('show ip ospf int brief\n')
        time.sleep(5)
        output = self.remote_conn.recv(1048576)
        ospf_rd = output.decode('utf-8')
        ospf_read = ospf_rd.split('\n')
        pattern_ospf = re.compile(r'(.+)( +)(.+)?(\d+)( +)(\d+)( +)(.+)( +)(\d+)( +)(.+)( +)(.+)')
        ospf_list = []
        host_raw = ospf_read[-1]
        host_temp = host_raw.split('#')
        hostname = host_temp[0] 
        for n, iface in enumerate(ospf_read):
            if n > 1 and iface != ospf_read[-1]:
                if '\\' not in iface and not iface.startswith(' '):
                    get_ospf = pattern_ospf.search(iface)
                    iface_ospf = get_ospf.group(1)
                    status = get_ospf.group(12)
                    ospf_iface = hostname + ',' + iface_ospf.strip() + ',' + status.strip()
                    ospf_list.append(ospf_iface)
                elif 'Se' in iface and '\\' in iface:
                    iface_merge = iface.strip() + ospf_read[n + 1].strip()
                    get_ospf = pattern_ospf.search(iface_merge)
                    seiface_ospf = get_ospf.group(1)
                    temp_iface = seiface_ospf.split(' ')
                    iface_ospf = temp_iface[0]
                    status = get_ospf.group(12)
                    ospf_iface = hostname + ',' + iface_ospf + ',' + status.strip()
                    ospf_list.append(ospf_iface)

        ospf_file = open('ospf_iface.txt','a+')
        for down_iface in ospf_list:
            ospf_file.write(down_iface + '\n')
            ospf_file.close()

#Example

Ip_File = input('Enter IP file name with extension: ')

ip_file_open = open(Ip_File,'r')

ip_list = ip_file_open.readlines()
print(ip_list)

for ip in ip_list:

        bgp_check = BgpStatus(ip)
        bgp_check.login()
        bgp_check.version()
        bgp_check.bgp_status() 


for ip in ip_list:

        ospf_check = OspfInt(ip)
        ospf_check.login()
        ospf_check.version()
        ospf_check.ospf_int_brief()
