#!/usr/bin/env python2
from base64 import b64decode
import email
import sys


def get_entries(files):
    msg = '-----\nCalendar entry from file {}\nID: {}\n-----'
    for path in files:
        with open(path) as f:
            mail = email.message_from_file(f)
            f.close()
            for part in mail.walk():
                if (part.get_content_subtype() == 'x-vnd.kolab.event'
                        and part.get('Content-Transfer-Encoding') == 'base64'):
                    print msg.format(path, mail.get('Subject'))
                    print b64decode(part.get_payload())

if __name__ == "__main__":
    get_entries(sys.argv[1:])
