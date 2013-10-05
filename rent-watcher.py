#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import pickle
import datetime
import os
import time

config = {
	"blitz": {
		"start_url": 'http://www.blitz-imobiliare.ro/inchirieri-apartamente-cluj/searchId=85209',
		"items": 'soup.find("ul", {"class": "productList"}).find_all("li")',
		"url": 'item.find("a")["href"]',
		"name": 'unicode(item.find("span", {"class": "prodName"}).string).strip()',
		"location": 'unicode(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()',
		"price": 'unicode(item.find("span", {"class": "prodPret"}).string).replace(u"€/luna", "").strip()',
		"next_url": 'soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]',
	},
	"welt": {
		"start_url": 'http://www.weltimobiliare.ro/search?to=rent&type=a2+h2&hood=1+19+26+48+49+32+50+51+52&price-max=270',
		"items": 'soup.find_all("li", {"class": "estate-listing"})',
		"url": '"http://www.weltimobiliare.ro" + item.find("h2").find("a")["href"]',
		"name": 'unicode(item.find("ul", {"class": "details"}).find("li").find("b").string).strip()',
		"location": 'unicode(item.find("ul", {"class": "details"}).find("li").next_sibling.next_sibling.find("b").next_sibling.string).replace(":", "").strip()',
		"price": 'unicode(item.find("ul", {"class": "details"}).find("span", {"class": "price"}).find("b").string).replace(u"Â €/luna", "").strip()',
		"next_url": '"http://www.weltimobiliare.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]',
	},
	"edil": {
		"start_url": 'http://www.edil.ro/actions/getOferte.php?jud=CJ&contract=2&imobil=1&nr_cam=2&imobil_nou=0&data=1&sort_2=1&st_limit=0&l=ro',
		"items": 'soup.find_all("div", {"class": "line-content"})',
		"url": '"http://www.edil.ro/" + item.find("div", {"class": "line-content-img"}).find("a")["href"]',
		"name": 'unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[0].find("p").find("a").string).strip()',
		"location": 'unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[3].find("p").string).replace("CLUJ-NAPOCA,", "").strip()',
		"price": 'unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[1].find("p").find("font").string).strip()',
		"next_url": 'http://www.edil.ro/actions/getOferte.php?jud=CJ&contract=2&imobil=1&nr_cam=2&imobil_nou=0&data=1&sort_2=1&st_limit=%d&l=ro',
	},
	"chirii": {
		"start_url": 'http://www.chirii-cluj.ro/search?type=sn+s+a2+h2&hood=1+19+26+48+49+32+50+51+52&price-max=270',
		"items": 'soup.find_all("li", {"class": "listing"})',
		"url": '"http://www.chirii-cluj.ro" + item.find("h2").find("a")["href"]',
		"name": 'unicode(item.find("h2").find("a").string).strip()',
		"location": 'unicode("")',
		"price": 'unicode(item.find("div", {"class": "property_price"}).find("a").string).replace(u"Price: €", "").replace("/month", "").strip()',
		"next_url": '"http://www.chirii-cluj.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]',
	},
}

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
		os.system('zenity --warning --title="rent-watcher alert" --text="Update(s) available" &')
	else:
		os.system('zenity --info --title="rent-watcher status" --text="Run ok, nothing new" &')

	print "Going to bed... ZzZzZzZzZzZzzz"
	time.sleep(666)

#==================================================================================================
