#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import re

r = requests.get("http://localhost/da.html")
soup = bs4.BeautifulSoup(r.text, "html5lib")
pad = 13

#================================================================================================== BLITZ

#items = soup.find("ul", {"class": "productList"}).find_all("li")
#item = items[0]
#print "url".ljust(pad) + item.find("a")["href"]
#print "name".ljust(pad) + unicode(item.find("span", {"class": "prodName"}).string).strip()
#print "location".ljust(pad) + unicode(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()
#print "price".ljust(pad) + unicode(item.find("span", {"class": "prodPret"}).string).replace(u"€/luna", "").strip()
#print "next_url".ljust(pad) + soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]

#================================================================================================== WELT

#items = soup.find_all("li", {"class": "estate-listing"})
#item = items[0]
#print "url".ljust(pad) + "http://www.weltimobiliare.ro" + item.find("h2").find("a")["href"]
#print "name".ljust(pad) + unicode(item.find("ul", {"class": "details"}).find("li").find("b").string).strip()
#print "location".ljust(pad) + unicode(item.find("ul", {"class": "details"}).find("li").next_sibling.next_sibling.find("b").next_sibling.string).replace(":", "").strip()
#print "price".ljust(pad) + unicode(item.find("ul", {"class": "details"}).find("span", {"class": "price"}).find("b").string).replace(u"Â €/luna", "").strip()
#print "next_url".ljust(pad) + "http://www.weltimobiliare.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]

#================================================================================================== EDIL

#items = soup.find_all("div", {"class": "line-content"})
#item = items[0]
#print "url".ljust(pad) + "http://www.edil.ro/" + item.find("div", {"class": "line-content-img"}).find("a")["href"]
#print "name".ljust(pad) + unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[0].find("p").find("a").string).strip()
#print "location".ljust(pad) + unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[3].find("p").string).replace("CLUJ-NAPOCA,", "").strip()
#print "price".ljust(pad) + unicode(item.find("div", {"class": "line-content-details"}).find_all("td")[1].find("p").find("font").string).strip()
#print "next_url".ljust(pad) + "http://www.edil.ro/actions/getOferte.php?jud=CJ&contract=2&imobil=1&nr_cam=1&imobil_nou=0&data=1&sort_2=1&st_limit=%d&l=ro"

#================================================================================================== CHIRII CLUJ

#items = soup.find_all("li", {"class": "listing"})
#item = items[0]
#print "url".ljust(pad) + "http://www.chirii-cluj.ro" + item.find("h2").find("a")["href"]
#print "name".ljust(pad) + unicode(item.find("h2").find("a").string).strip()
#print "location".ljust(pad) + unicode("")
#print "price".ljust(pad) + unicode(item.find("div", {"class": "property_price"}).find("a").string).replace(u"Price: €", "").replace("/month", "").strip()
#print "next_url".ljust(pad) + "http://www.chirii-cluj.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]

#================================================================================================== END

















