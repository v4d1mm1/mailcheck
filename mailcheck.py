import smtplib
import dns.resolver
import sys
from logging_setup import logging
from logging import config
from pathlib import Path

HELO_FROM_DOMAIN = 'mailbox.org'

def resolve_mx_record(domain):
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
        exit(logging.error(ex))
    server.mail('')
    code, message = server.rcpt(email_address)
    logging.info(f'Checked {email_address}. Response code: {code}. Message: {message}')
    file_logger.info(f'Checked {email_address}. Response code: {code}. Message: {message}')
    return code, message

   
if __name__ == "__main__":
    # Apply logging config file
    try:
        script_dir = Path(__file__).resolve().parent
        file_path = script_dir / "logging.config"

        with open(file_path, 'r') as file:
            config.fileConfig(file)

    except FileNotFoundError:
        logging.error('Logging config file was not found in the same directory as the script')

    file_logger = logging.getLogger('customLogger')

    # Get email address either from sys arg or input
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

