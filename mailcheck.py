import smtplib
import dns.resolver
import sys

try:
    email_address = sys.argv[1]
except Exception as ex:
    email_address = input('Email to check: ')

if '@' in email_address:
    domain = email_address.split('@')[1]
else:
    sys.exit('Error: email entered incorrectly')

try:
    records = dns.resolver.resolve(domain, 'MX')
except Exception as ex:
    exit(ex)

mx_record = records[0].exchange
mx_record = str(mx_record)
print('MX record:', mx_record)

server = smtplib.SMTP()
server.set_debuglevel(0)

try:
    server.connect(mx_record)
    code, message = server.helo('mailbox.org')    
except Exception as ex:
    print(ex) 

server.mail('')

code, message = server.rcpt(email_address)

print('Response code:', code)
print('Response message:', message)