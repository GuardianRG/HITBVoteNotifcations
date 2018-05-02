import requests, re, sys
from bs4 import BeautifulSoup

def push(title,message):
	push = requests.post("https://api.pushover.net/1/messages.json", data = {"token": "APPTOKEN", "user": "USERTOKEN",  "message": message, "title":title})

adict = {}

while (True):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
		r = requests.get('https://gsec.hitb.org/vote/', headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")
		finalpush = ""
	except:
		continue

	for table in soup.findAll("table", class_="paper_list"):
		for tr in table.findAll("tr"):
				paper = ""
				author = ""
				votes = 0
				for i, td in enumerate(tr.findAll("td")):
					if i == 0:
						paper = td.text
					elif i == 1:
						author = td.text
					else:
						votes = int(td.text)

				if author == "":
					continue
				#print "{} - {}".format(author,votes)
				if not(hash(paper) in adict):
					# if paper does not already exist, add it
					adict[hash(paper)] = {"paper":paper, "author":author, "votes": votes}
					finalpush += "{} - {} votes\r\n".format(author, votes)
				else:
					# paper already in dictionary
					# Do the checking logic to last run
					oldvotes = adict[hash(paper)]["votes"]
					if oldvotes != votes:
						# vote changed
						if oldvotes < votes:
							finalpush += "[+] {} - {} votes\r\n".format(author,votes)
						else:
							finalpush += "[-] {} - {} votes\r\n".format(author,votes)
							
						adict[hash(paper)]["votes"] = votes
	
	if finalpush != "":
		push("Votes Changed", finalpush)
		
	