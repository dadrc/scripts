#!/usr/bin/env python2
from base64 import b64decode
import email
import sys


def get_entries(files):
    for path in files:
        with open(path) as f:
            msg = email.message_from_file(f)
            f.close()
            print "-----\nCalendar entry from file {}\nID: {}\n-----".format(
                path,
                msg.get('Subject')
            )
            for part in msg.walk():
                if part.get_content_subtype() == 'x-vnd.kolab.event':
                    print b64decode(part.get_payload())

if __name__ == "__main__":
    get_entries(sys.argv[1:])
