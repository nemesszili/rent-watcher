#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import pickle
import datetime
import os

#================================================================================================== BLITZ

def get_blitz(start_url, results, new_urls, paginate=True):
	urls = [start_url]
	new_urls = []
	while len(urls) > 0:
		url = urls.pop()
		print url
		r = requests.get(url)
		soup = bs4.BeautifulSoup(r.text, "html.parser")
		items = soup.find("ul", {"class": "productList"}).find_all("li")
		print "  %d items" % len(items)

		new = 0
		for item in items:
			url = item.find("a")["href"]
			name = unicode(item.find("span", {"class": "prodName"}).string).strip()
			location = unicode(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()
			price = unicode(item.find("span", {"class": "prodPret"}).string).strip()
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
			try:
				next_page = soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]
			except Exception:
				next_page = None
			if next_page != None:
				urls.append(next_page)

	return (results, new_urls)

#================================================================================================== LOAD, FETCH, SAVE

if not os.path.isfile("results.pickle"):
	results = {}
else:
	results = pickle.load(open("results.pickle", "rb"))
new_urls = []

results, new_urls = get_blitz("http://www.blitz-imobiliare.ro/inchirieri-apartamente-cluj/searchId=83936", results, new_urls)

pickle.dump(results, open("results.pickle", "wb"))

#================================================================================================== BUILD REPORT

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

#==================================================================================================
