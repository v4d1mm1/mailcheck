import smtplib
import dns.resolver
import sys
import logging

HELO_FROM_DOMAIN = 'mailbox.org'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S') 

def resolve_mx_record(domain):
    mx_record = ''
    try:
        records = dns.resolver.resolve(domain, 'MX')
    except Exception as ex:
        exit(logging.error(ex))
    mx_record = records[0].exchange
    mx_record = str(mx_record)
    logging.info(f'Found MX record {mx_record}')
    return mx_record

def check_mail(email_address, mx_record):
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    try:
        server.connect(mx_record)
        code, message = server.helo(HELO_FROM_DOMAIN)    
    except Exception as ex:
        print(logging.error(ex)) 
    server.mail('')
    code, message = server.rcpt(email_address)
    logging.info(f'Checked {email_address} on {domain}. Response code: {code}. Message: {message}')
    return code, message
    
if __name__ == "__main__":
    try:
        email_address = sys.argv[1]
    except Exception as ex:
        email_address = input('Email to check: ')
    if '@' in email_address:
        mailbox, domain = email_address.split('@')
        logging.info(f'Checking {email_address}...')
    else:
        sys.exit(logging.error('Email entered incorrectly'))    
  
    mx_record = resolve_mx_record(domain)
    check_mail(email_address, mx_record)