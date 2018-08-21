import smtplib
from email.mime.text import MIMEText

#with smtplib.SMTP('localhost') as s:
#	s.sendmail('John.Bradshaw2@traviscountytx.gov', 'John.Bradshaw2@traviscountytx.gov', "This is a test message")
#	s.quit()

msg = MIMEText("This is a test")
msg['Subject'] = "Test"
msg['From'] = "John.Bradshaw@secops-virtual-machine"
msg['To'] = "John.Bradshaw2@traviscountytx.gov"

with smtplib.SMTP('localhost') as s:
	s.send_message(msg)
	s.quit()

