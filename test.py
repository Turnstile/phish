from ldapserver import LDAPServer
import requests, json, urllib3
import configparser
import ldapserver
import sys
import smtplib
from email.mime.text import MIMEText
import dateutil.parser
from datetime import datetime, timezone

#defaults from config
config = configparser.ConfigParser()
config.read('config.ini')
server = config['Default']['Server']
username = config['Default']['Username'] 
password = config['Default']['Password']
token = config['Default']['Auth Token']
sender = config['Default']['Sender']
recipient = config['Default']['Recipient']

#disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#authorization header
authJson = { 
	'Authorization': token,
	'content-type': 'application/json'
	}

url = 'https://its-ptr01-p/api/lists/15/members.json'
b9StrongCert = False	

#request compromised users
r = requests.get(url, headers=authJson, verify=b9StrongCert)
users = r.json() 

#if no users need to be deactivated, exit
if not users:
	#print("No phishes found")
	#TODO for testing only, uncomment
	sys.exit()

#create list of users to be deactivated, in the form of (id, username)
deactivate_list = []
for user in users:
	#if user is expired, remove from list
	exp = dateutil.parser.parse(user['expiration'])
	current = datetime.now(timezone.utc)
	if current > exp:
		url = 'https://its-ptr01-p/api/lists/15/members/' + str(user['id']) + '.json'
		r = requests.delete(url, headers=authJson, verify=b9StrongCert)
	
	#otherwise add user to deactivate list 
	else:
		deactivate_list.append((user['id'], user['reverse_user']['username']))

#TODO for testing only, remove
#deactivate_list = [(0, 'BradshJ1')]
#print(deactivate_list)

#open connection to eDirectory
#s = LDAPServer(server, username, password)

#for user in deactivate_list:
	#build distinguished name
#	dn = 'cn=' + user[1] + ',ou=internal,ou=cnusers,o=travis_auth'
	#print(dn)
	#get user information for email
#	s.get_user(dn)
	#print(s.conn.entries)
#	user_info = s.conn.entries[0]
	#disable the user
#	s.disable_user(dn)
	#remove user from list
#	url = 'https://its-ptr01-p/api/lists/15/members/' + str(user[0]) + '.json'
#	r = requests.delete(url, headers=authJson, verify=b9StrongCert)
	#function to determine if data is missing
#	xstr = lambda s: 'Not Found' if s is None else str(s)
	#send email for changegear ticket
#	msg = MIMEText("User's account has been disabled to protect personal information, please contact the user and reset their password.\nUsername: " + user[1] + "\nFirst Name: "  + xstr(user_info['givenName']) + "\nLast Name: " + xstr(user_info['sn']) + "\nPhone Number: " + xstr(user_info['telephoneNumber']))
#	msg['Subject'] = "Phishing Password Reset"
#	msg['From'] = sender
#	msg['To'] = recipient
#	msg['Cc'] = "HD-Techs@traviscountytx.gov,SecOps@traviscountytx.gov"	

#	with smtplib.SMTP('localhost') as sm:
#		sm.send_message(msg)
#		sm.quit()
	

#close eDirectory connection	
#s.close_connection()


