#!/usr/bin/env python2
from base64 import b64decode
import email
import sys


def get_mail(files):
    for path in files:
        with open(path) as f:
            get_entry(path, email.message_from_file(f))
            f.close()


def get_entry(path, mail):
    msg = '-----\nCalendar entry from file {}\nID: {}\n-----'
    for part in mail.walk():
        if (part.get_content_subtype() == 'x-vnd.kolab.event'
                and part.get('Content-Transfer-Encoding') == 'base64'):
            print msg.format(path, mail.get('Subject'))
            print b64decode(part.get_payload())


if __name__ == "__main__":
    get_mail(sys.argv[1:])
