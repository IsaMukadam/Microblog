import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("This is a test email.")
msg['Subject'] = 'Test'
msg['From'] = 'test@localhost'
msg['To'] = 'admin@example.com'

with smtplib.SMTP('localhost', 8025) as server:
    server.send_message(msg)

# Have to open port 8025 or allow python to access through the firewall 
# ERROR: ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it