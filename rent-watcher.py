#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import requests
import bs4
import pickle
import os
import pystache
import smtplib
import time
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from rent_conf import *

#================================================================================================== GET DATA

def get_data(site, results, paginate=True, recent=None):
    new_urls = []
    time = datetime.now()
    urls = [config[site]["start_url"]]
    last_url = config[site]["start_url"]
    page = 0
    while len(urls) > 0:
        url = urls.pop()
        print url

        r = requests.get(url)
        if url != config[site]["start_url"]:
            if r.text == last_page:
                break
        last_page = r.text

        soup = bs4.BeautifulSoup(r.text, "html5lib")
        items = eval(config[site]["items"])
        print "  %d items" % len(items)

        new = 0
        for item in items:
            url_func = config[site]["url"]
            url = url_func(item) if callable(url_func) else eval(url_func)
            name = eval(config[site]["name"])
            location = eval(config[site]["location"])
            price = eval(config[site]["price"])
            if url not in results:
                new += 1
                results[url] = {
                    "name": name,
                    "location": location,
                    "price": price,
                    "time": time,
                }
                new_urls.append(url)
        print "  %d new" % new

        if paginate:
            page += 1
            try:
                if site.find("edil") != -1:
                    next_url = config[site]["next_url"] % page
                else:
                    next_url = eval(config[site]["next_url"])
            except Exception:
                next_url = None
            if next_url != None and next_url != last_url:
                urls.append(next_url)
                last_url = next_url

    return (results, new_urls)

def get_recent(results, since):
    return [url for url, info in results.items() if info['time'] > since]

#================================================================================================== LOAD, FETCH, SAVE, BUILD REPORT, SLEEP


def sendemail(from_addr, to_addr_list,
              subject, message,
              login=None, password=None,
              smtpserver='smtp.gmail.com:587'):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr_list)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText('this is a text only preview, does your email support html ?', 'plain')
    part2 = MIMEText(message, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP(smtpserver)
    if login and password:
        server.starttls()
        server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, msg.as_string())
    server.quit()

def email_report(to=EMAIL_TO, html_file='zeh_report.html'):
    message = open(html_file).read()
    sendemail(from_addr='nemutam@stirbu.name', to_addr_list=to,
              subject='Ne mutam!', message=message,
              smtpserver=SMTP_SERVER)

def show_results(new_urls):
    if len(new_urls) != 0:
        now_str = str(datetime.now())[:19]

        mobile_url = lambda url: (url.replace('www', 'm').replace('oras-cluj-napoca/', '')
                                  if url is not None and 'piata-az' in url
                                  else url)
        offers = [{'url': mobile_url(url),
                   'name': results[url]['name'],
                   'location': results[url]['location'],
                   'price': results[url]['price'],
                   } for url in new_urls]
        context = {'date': str(datetime.now())[:19],
                   'offers': offers}
        
        r = pystache.Renderer()
        report = r.render_path('report_tmpl.html', context)
        with codecs.open('zeh_report.html', 'w', encoding='utf-8') as report_f:
            report_f.write(report)

        email_report()

        os.system('zenity --warning --title="rent-watcher alert" --text="Update(s) available" &')


# since = yesterday = datetime.now() - timedelta(days=1)
since = None

while True:
    if not os.path.isfile("results.pickle"):
        results = {}
    else:
        results = pickle.load(open("results.pickle", "rb"))
        # sorted_results = sorted([url, info for url, info in results.items()]
        #                         key=lambda url_info: url_info[1].get('time', None))

    new_urls = []
    for site in config:
        try:
            results, more_new_urls = get_data(site, results)
            new_urls += more_new_urls
        except requests.exceptions.RequestException as e:
            print "Error " + str(e)

        if since:
            new_urls += get_recent(results, since)
            since = None

    try:
        show_results(new_urls)
        pickle.dump(results, open("results.pickle", "wb"))
    except Exception as e:
        print "Error: %s" % e
        traceback.print_stack()


    print "Going to bed... ZzZzZzZzZzZzzz"
    time.sleep(666)

#==================================================================================================
