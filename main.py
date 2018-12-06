#!/usr/bin/env python2

import argparse
import sys
import re
import requests
from HTMLParser import HTMLParser


def web_request(website):
    """This is a handler """
    print(website)
    r = requests.get(website)

    parser = MyParser()
    parser.feed(r.content)
    phone_scrape(parser.data_in_tags)
    email_scrape(parser.data_in_tags)
    url_scrape(parser.url_to_scrape)


def phone_scrape(website):
    s = '1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?'
    phone_numbers = re.findall(
        s, website)
    print
    print("Phone Numbers:")
    parsed_number = []
    for item in phone_numbers:
        area, mid, last, x, y = item
        corrected_number = area + '-' + mid + '-' + last
        if corrected_number not in parsed_number:
            print corrected_number
        parsed_number.append(corrected_number)


def url_scrape(website):
    # given options, looks for website
    # Divided regiex in half to meet the pep8 requirement
    first_half = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
    second_half = '(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    other_links = re.findall(
        first_half + second_half, website)
    print
    print("URL's")
    unique_handling = []
    for url in other_links:
        if url not in unique_handling:
            print(url)
            unique_handling.append(url)
    return other_links


def email_scrape(website):
    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+', website)
    print
    print("Emails")
    already_printed = []
    for email in emails:
        if email not in already_printed:
            print(email)
            already_printed.append(email)
    print


def source_url(attrs):
    for name, value in attrs:
        if 'src' or 'href' in name:
            return value
        else:
            return ''


class MyParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_script = False
        self.url_to_scrape = ''
        self.data_in_tags = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a' or tag == 'img':
            self.url_to_scrape += source_url(attrs) + ' '
        if tag == 'script':
            self.in_script = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False

    def handle_data(self, data):
        if not self.in_script:
            if data:
                self.data_in_tags += data + ' '


def create_parser():
    parser = argparse.ArgumentParser(description='Scrape a website')
    parser.add_argument(
        'url', help='Provide a website to scrape', nargs='+')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    if args.url:
        web_request(args.url[0])


if __name__ == "__main__":
    main()
    pass


# get urls only from a, href, and image tags -
# get phone numbers only from in between tags, not from attributes
# ignore all script sources because instructions unclear
#  usehtml parser ignore beautiful soup for now
