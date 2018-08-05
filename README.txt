
You can use this scripts to get the desired information or to push bulk configuration to multiple cisco devices at the same time and the speciality of this scripts are everything in one place so its easy to manage.

I used python classes and methods to do this and you can improve the code by adding more functionality in the same script for better use

NOTE: these scripts recommended to run in python3.6

Packages need to be installed.


paramiko

By using this script you can achive the following.

	1. Check the BGP status of the links

	2. Check the 'DOWN' interface which is running OSPF


login_version.py 

This script is common to every device and it will to 2 tasks.

	1. Login to the device 
		we can use multiple credential for login.

		 [('username1', 'password1', 'secret1'), ('username2', 'password2', 'secret2'),                        ('username3', 'password3', 'secret3')]

		 you can specify multiple username , password and enable password/secret in above mentioned place for login purpose

	2. Check the IOS version

		it will run 'show version' command and get you the IOS version and based on that you can determine your next commands for your needs.

master_config.py

As off now i have  created 2 function for the following

	1. BGP
		to check bgp status of a device

	2. OSPF

		to check the 'DOWN' interface in all ospf running interfaces.


HOW TO USE

copy all the files in one directory

put the credentials in login_version.py as mentioned above.

mention all the ip address in the ip_list.txt file one by one as mentioned below

ex:

10.1.1.1
10.1.1.2
10.1.1.3

run the script in a terminal

ex:

python3.6 master_config.py 

