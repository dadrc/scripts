#!/usr/bin/env python2
from base64 import b64decode
import email
import sys
import argparse
from collections import namedtuple

Mail = namedtuple("Mail", "path content")


def get_mails(files):
    mails = list()
    for path in files:
        with open(path) as f:
            mails.append(Mail(path, email.message_from_file(f)))
            f.close()
    return mails


def print_entry(part, mail, header):
    if header:
        msg = '-----\nPart from file {}\nID: {}\n-----'
        print msg.format(mail.path, mail.content.get('Subject'))
    if (part.get('Content-Transfer-Encoding') == 'base64'):
        print b64decode(part.get_payload())
    else:
        print part.get_payload()


def get_entry(mail, subtype, filename, header, base64, nobase64):
    printed = 0
    for part in mail.content.walk():
        partname = part.get_filename().lower() if part.get_filename() else ''
        if ((not subtype or subtype in part.get_content_subtype()) and
                (not filename or partname == filename.lower())):
            isbase64 = (part.get('Content-Transfer-Encoding') == 'base64')
            if ((isbase64 and base64) or
                    (not isbase64 and nobase64) or
                    (not base64 and not nobase64)):
                printed += 1
                print_entry(part, mail, header)
    return printed


def main():
    parser = argparse.ArgumentParser(
        description='Gets attachments from mail files.')
    parser.add_argument('-t', '--subtype', metavar='TYPE',
                        help='Only print parts with subtype TYPE')
    parser.add_argument('-f', '--filename', metavar='NAME',
                        help='Only print attachments with filename NAME')
    parser.add_argument('-b', '--base64', action='store_true',
                        help='print only base64-encoded parts')
    parser.add_argument('-B', '--nobase64', action='store_true',
                        help='skip base64-encoded parts')
    parser.add_argument('--header', action='store_true',
                        help='print information about the mail')
    parser.add_argument('files', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    # no filename given
    if not len(sys.argv) > 1:
        parser.print_help()
        exit(2)
    printed = 0
    mails = get_mails(args.files)
    for mail in mails:
        printed += get_entry(mail, args.subtype, args.filename,
                             args.header, args.base64, args.nobase64)
    exit(0 if printed > 0 else 1)


if __name__ == "__main__":
    main()
