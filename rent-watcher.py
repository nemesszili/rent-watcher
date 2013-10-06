#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import pickle
import datetime
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rent_conf import *

#================================================================================================== GET DATA

def get_data(site, results, new_urls, paginate=True):
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
			url = eval(config[site]["url"])
			name = eval(config[site]["name"])
			location = eval(config[site]["location"])
			price = eval(config[site]["price"])
			if url not in results:
				new += 1
				results[url] = {
					"name": name,
					"location": location,
					"price": price,
				}
				new_urls.append(url)
		print "  %d new" % new

		if paginate:
			page += 1
			try:
				if site == "edil":
					next_url = config[site]["next_url"] % page
				else:
					next_url = eval(config[site]["next_url"])
			except Exception:
				next_url = None
			if next_url != None and next_url != last_url:
				urls.append(next_url)
				last_url = next_url

	return (results, new_urls)

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
    sendemail(from_addr='nemutam@gmail.com', to_addr_list=to,
              subject='Ne mutam!', message=message,
              smtpserver=SMTP_SERVER)


while True:
	if not os.path.isfile("results.pickle"):
		results = {}
	else:
		results = pickle.load(open("results.pickle", "rb"))
	new_urls = []

	for site in config:
		results, new_urls = get_data(site, results, new_urls)
		pickle.dump(results, open("results.pickle", "wb"))

	if len(new_urls) != 0:
		f = open("results.html", "a")
		s = '''<div class="update">%s</div>
	<table>
	''' % str(datetime.datetime.now())[:19]
		f.write(s)
		for url in new_urls:
			s = '''	<tr>
			<td><a href="%s">%s</a></td>
			<td>%s</td>
			<td>%s</td>
		</tr>
	''' % (url, results[url]["name"], results[url]["location"], results[url]["price"])
			f.write(s.encode("utf8"))

		s = '''</table>
	'''
		f.write(s)
		f.close()
		os.system("cat report_head.html results.html report_body.html > zeh_report.html")

		email_report()

		os.system('zenity --warning --title="rent-watcher alert" --text="Update(s) available" &')
	else:
		os.system('zenity --info --title="rent-watcher status" --text="Run ok, nothing new" &')

	print "Going to bed... ZzZzZzZzZzZzzz"
	time.sleep(666)

#==================================================================================================
