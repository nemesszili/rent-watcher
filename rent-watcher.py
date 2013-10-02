#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4

r = requests.get("http://localhost/da.html")

soup = bs4.BeautifulSoup(r.text, "html.parser")
items = soup.find("ul", {"class": "productList"}).find_all("li")
results = {}

for item in items:
	url = item.find("a")["href"]
	name = unicode(item.find("span", {"class": "prodName"}).string).strip()
	location = unicode(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()
	price = unicode(item.find("span", {"class": "prodPret"}).string).strip()
	if url not in results:
		results[url] = {
			"name": name,
			"location": location,
			"price": price,
		}

try:
	next_page = soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]
except Exception:
	next_page = None
