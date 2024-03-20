import logging
import re

logging.basicConfig(level=logging.INFO) 

class ResultsFilter(logging.Filter):
    def filter(self, record):
        # Filter out OK responses
        return 'code: 250' not in record.getMessage()

class CustomFileHandler(logging.Handler):
    EMAIL_REGEX = r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'
    OBFUSCATE = 1   
    TOP_DOMAINS = {'gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'hotmail.co.uk', 'hotmail.fr', 'msn.com', 
               'yahoo.fr', 'wanadoo.fr', 'orange.fr', 'comcast.net', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.co.in', 
               'live.com', 'rediffmail.com', 'free.fr', 'gmx.de', 'web.de', 'yandex.ru', 'ymail.com', 'libero.it', 
               'outlook.com', 'uol.com.br', 'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 'sbcglobal.net', 'sfr.fr', 
               'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 'yahoo.es', 'ig.com.br', 'live.nl', 'bigpond.com', 
               'terra.com.br', 'yahoo.it', 'neuf.fr', 'yahoo.de', 'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 
               'facebook.com', 'bellsouth.net', 'yahoo.in', 'hotmail.es', 'charter.net', 'yahoo.ca', 'yahoo.com.au', 
               'rambler.ru', 'hotmail.de', 'tiscali.it', 'shaw.ca', 'yahoo.co.jp', 'sky.com', 'earthlink.net', 'optonline.net', 
               'freenet.de', 't-online.de', 'aliceadsl.fr', 'virgilio.it', 'home.nl', 'qq.com', 'telenet.be', 'me.com', 
               'yahoo.com.ar', 'tiscali.co.uk', 'yahoo.com.mx', 'voila.fr', 'gmx.net', 'mail.com', 'planet.nl', 'tin.it', 
               'live.it', 'ntlworld.com', 'arcor.de', 'yahoo.co.id', 'frontiernet.net', 'hetnet.nl', 'live.com.au', 
               'yahoo.com.sg', 'zonnet.nl', 'club-internet.fr', 'juno.com', 'optusnet.com.au', 'blueyonder.co.uk', 
               'bluewin.ch', 'skynet.be', 'sympatico.ca', 'windstream.net', 'mac.com', 'centurytel.net', 'chello.nl', 
               'live.ca', 'aim.com', 'bigpond.net.au'}
        
    def __init__(self, filename, mode='a', encoding='utf-8', delay=False, obfuscate=None, top_domains=None):
        logging.Handler.__init__(self)
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.stream = None
        self.addFilter(ResultsFilter())
        self.obfuscate = obfuscate if obfuscate is not None else self.OBFUSCATE
        self.top_domains = top_domains if top_domains is not None else self.TOP_DOMAINS

    def emit(self, record):
        try:
            if self.stream is None:
                self.stream = open(self.filename, self.mode, encoding=self.encoding)
            msg = self.format(record)
            obfuscated_msg = self.obfuscate_emails(msg) if self.obfuscate else msg
            self.stream.write(obfuscated_msg + '\n')
            self.flush()
        except Exception:
            self.handleError(record)

    def obfuscate_emails(self, msg):
        def replace_email(match):
            mailbox = match.group(1)
            domain = match.group(2)
            obfuscated_mailbox = mailbox[:len(mailbox) // 2] + '*' * (len(mailbox) // 2)
            # No reason to obfuscate if domain is among top domains
            if domain not in self.TOP_DOMAINS:
                obfuscated_domain = '*' * (len(domain) // 2) + domain[len(domain) // 2:]
            else:
                obfuscated_domain = domain
            return obfuscated_mailbox + '@' + obfuscated_domain

        # Replace emails with obfuscated first half
        return re.sub(self.EMAIL_REGEX, replace_email, msg)

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        logging.Handler.close(self)

root_logger = logging.getLogger()
file_handler = CustomFileHandler('mailcheck.log')
root_logger.addHandler(file_handler)
