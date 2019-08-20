import smtplib, ssl
from email.mime.text import MIMEText
import argparse
import sys
import colorama
from colorama import Fore, Back, Style
colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument('-subject', '-s', help='subject to send email with')
parser.add_argument('-to', help='person to send email to')
args = parser.parse_args()

def run():
    patches = sys.stdin.read()
    s = patches

    FROM = 'linuxsysdemo@gmail.com'
    TO = 'linuxsysdemo@gmail.com'
    password = 'password11235!'

    msg = MIMEText(s)

    msg['Subject'] = args.subject
    msg['From'] = FROM
    msg['To'] = TO

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(FROM, password)
        server.sendmail(
            FROM, TO, msg.as_string()
        )
        server.quit()

    print(Fore.LIGHTCYAN_EX + "Email sent successfully to " + TO + Style.RESET_ALL)

if __name__ == '__main__':
    run()
