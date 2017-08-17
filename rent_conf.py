# -*- coding: utf-8 -*-

EMAIL_TO = ['nemesszili@gmail.com']            # only gmail is supported, see below
SMTP_SERVER = 'gmail-smtp-in.l.google.com'  # incoming mail, accepts only gmail

def mercador_url(item):
    a = item.find("a", {"class": "detailsLink"})
    if a is not None:
        return a['href']
    else:
        print('mercador_url: %s' % a)

config = {
	# "blitz": {
	# 	"start_url": 'http://www.blitz-imobiliare.ro/inchirieri-apartamente-cluj/searchId=85206',
	# 	"items": 'soup.find("ul", {"class": "productList"}).find_all("li")',
	# 	"url": 'item.find("a")["href"]',
	# 	"name": 'str(item.find("span", {"class": "prodName"}).string).strip()',
	# 	"location": 'str(item.find("span", {"class": "sgreen"}).next_sibling.string).strip()',
	# 	"price": 'str(item.find("span", {"class": "prodPret"}).string).strip()',
	# 	"next_url": 'soup.find("div", {"class": "pageNav"}).find("a", {"class": "active"}).parent.next_sibling.find("a")["href"]',
	# },
	"nemutam": {
		"start_url": 'https://nemutam.com',
		"items": 'soup.find_all("div", {"class": "col-xs-12 col-md-6 col-lg-4"})',
		"url": 'item.find("div", {"class": "post"}).find("a")["href"]',
		"name": 'str(item.find("div", {"class": "caption"}).find("p").string).strip()',
		"location": 'str(item.find("div", {"class": "caption"}).find_all("td")[1].string).strip()',
		"rooms": 'str(item.find("div", {"class": "caption"}).find_all("td")[3].string).strip()',
		"price": 'str(item.find("span", {"class": "post-price"}).string).strip()',
		"next_url": '"https://nemutam.com" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]',
	},
	# "welt": {
	# 	"start_url": 'http://www.weltimobiliare.ro/search?to=rent&type=s+a3&hood=1+19+26+28+48+49+30+32+50+51+52&price-max=450',
	# 	"items": 'soup.find_all("li", {"class": "estate-listing"})',
	# 	"url": 'item.find("h2").find("a")["href"]',
	# 	"name": 'str(item.find("ul", {"class": "details"}).find("li").find("b").string).strip()',
	# 	"location": 'str(item.find("ul", {"class": "details"}).find("li").next_sibling.next_sibling.find("b").next_sibling.string).replace(":", "").strip()',
	# 	"price": 'str(item.find("ul", {"class": "details"}).find("span", {"class": "price"}).find("b").string).strip()',
	# 	"next_url": '"http://www.weltimobiliare.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]',
	# },
	# "edil-apartamente3": {
	# 	"start_url": 'http://www.edil.ro/actions/getOferte.php?jud=CJ&contract=2&imobil=1&nr_cam=3&imobil_nou=0&data=1&sort_2=1&st_limit=0&l=ro',
	# 	"items": 'soup.find_all("div", {"class": "line-content"})',
	# 	"url": '"http://www.edil.ro/" + item.find("div", {"class": "line-content-img"}).find("a")["href"]',
	# 	"name": 'str(item.find("div", {"class": "line-content-details"}).find_all("td")[0].find("p").find("a").string).strip()',
	# 	"location": 'str(item.find("div", {"class": "line-content-details"}).find_all("td")[3].find("p").string).replace("CLUJ-NAPOCA,", "").strip()',
	# 	"price": 'str(item.find("div", {"class": "line-content-details"}).find_all("td")[1].find("p").find("font").string).strip()',
	# 	"next_url": 'http://www.edil.ro/actions/getOferte.php?jud=CJ&contract=2&imobil=1&nr_cam=1&imobil_nou=0&data=1&sort_2=1&st_limit=%d&l=ro',
	# },
	# "chirii-cluj": {
	# 	"start_url": 'http://www.chirii-cluj.ro/search?type=s+a1+a2&hood=1+19+26+28+48+49+30+32+50+51+52&price-max=270',
	# 	"items": 'soup.find_all("li", {"class": "listing"})',
	# 	"url": '"http://www.chirii-cluj.ro" + item.find("h2").find("a")["href"]',
	# 	"name": 'str(item.find("h2").find("a").string).strip()',
	# 	"location": 'str("")',
	# 	"price": 'str(item.find("div", {"class": "property_price"}).find("a").string).strip()',
	# 	"next_url": '"http://www.chirii-cluj.ro" + soup.find("li", {"class": "page selected"}).next_sibling.next_sibling.find("a")["href"]',
	# },
	# "piata-az-apartamente1": {
	# 	"start_url": 'http://www.piata-az.ro/anunturi/apartamente-1031?f_valuta=+70525&f_price=0%2C270&f_tip_oferta_inchirieri=+70410&f_imobiliare_camere=3',
	# 	"items": 'soup.find("div", {"class": "anunt list"}).find_all("div", {"class": "anunt"})',
	# 	"url": 'item.find("h3").find("a")["href"]',
	# 	"name": 'str(item.find("h3").find("a").string).strip()',
	# 	"location": 'str("")',
	# 	"price": 'str(item.find("span", {"class": "price"}).contents[0]).strip()',
	# 	"next_url": 'soup.find("div", {"class": "pagination"}).find("span", {"class": "current"}).next_sibling.next_sibling["href"]',
	# },
}

