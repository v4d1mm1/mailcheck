# mailcheck
Simple script to check email address. Accepts email address either from sys arg or input
___

### examples:
+ random20244654@gmail.com - will have response 550 and will be logged to file and not obfuscated (no reason to obfuscate if domain is among top domains).
+ johnsmith100@gmail.com - will have response 250 OK and will not be logged to file because of logging filter.
+ random20244654@protonmail.ch - will have response 550 and will be logged to file and obfuscated (obfuscation was added for company domains).