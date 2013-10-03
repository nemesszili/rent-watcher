#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import pickle
import datetime
import os

#================================================================================================== GET DATA

def get_data(site, results, new_urls, paginate=True):
	urls = [config[site]["start_url"]]
	while len(urls) > 0:
		url = urls.pop()
		print url
		r = requests.get(url)
		soup = bs4.BeautifulSoup(r.text, "html.parser")
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
			try:
				next_page = eval(config[site]["next_page"])
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

config = {
	"blitz": {
		"start_url": 'http://localhost/da.html',
		"items": 'soup.find("ul", {"class": "productList"}).find_all("li")',
		"url": 'item.find("a")["href"]',
		"name": 'unicode(item.find("span", {"class": "prodName"}).string).strip()',
		"location": 'unicode(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()',
		"price": 'unicode(item.find("span", {"class": "prodPret"}).string).strip()',
		"next_page": 'soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]',
	},
}

for site in config:
	results, new_urls = get_data(site, results, new_urls, False)

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
