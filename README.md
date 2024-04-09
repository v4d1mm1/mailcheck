# mailcheck
Simple script to check email address. Accepts email address either from command line argument or input.
___

Mailbox is always obfuscated by default in a log file.

### Examples:
+ johnsmith100@gmail.com - will have response 250 OK and will not be logged to file because of logging filter;
+ random20244654@gmail.com - will have response 550 and will be logged to file and domain will not be obfuscated (no reason to obfuscate if domain is among top domains);
+ random20244654@protonmail.ch - will have response 550 and will be logged to file and domain will be obfuscated (obfuscation was added for business's custom domain names).