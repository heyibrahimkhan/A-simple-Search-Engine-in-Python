#!/usr/bin/python
#Author : dileep98490@gmail.com
import urllib
from bs4 import BeautifulSoup
max_limit=5
def get_page(url):#This function is just to return the webpage contents; the source of the webpage when a url is given.
	try:
		f = urllib.urlopen(url)
		page = f.read()
		f.close()
		#print page
		return page
	except:	
		return ""
	return ""
def union(a,b):#The union function merges the second list into first, with out duplicating an element of a, if it's already in a. Similar to set union operator. This function does not change b. If a=[1,2,3] b=[2,3,4]. After union(a,b) makes a=[1,2,3,4] and b=[2,3,4]
	for e in b:
		if e not in a:
			a.append(e)
	return a;

def get_next_url(page):
	start_link=page.find("a href")
	if(start_link==-1):
		return None,0
	start_quote=page.find('"',start_link)
	end_quote=page.find('"',start_quote+1)
	url=page[start_quote+1:end_quote]
	return url,end_quote
def get_all_links(page):
	links=[]
	while(True):
		url,n=get_next_url(page)
		page=page[n:]
		if url:
			# print "url = "+url
			links.append(url)
		else:
			break
	return links
def Look_up(index,keyword):#This function is for given an index, it finds the keyword in the index and returns the list of links
	#f=[]
	# pages = [];
	# keywords = keyword.split();
	# for k in keywords:
	if keyword in index:
		return index[keyword]
		# if k in index:
		# 	pages.append(index[keyword]);
	return []
#The format of element in the index is <keyword>,[<List of urls that contain the keyword>]
def add_to_index(index,url,keyword):
	if keyword in index:
		if url not in index[keyword]:
			try:
				print "keyword = "+str(keyword)
				index[keyword].append(url)
			except:
				print " "
		return
	index[keyword]=[url]

def add_page_to_index(index,url,content):#Adding the content of the webpage to the index
	# Add function splitter here
	content = my_page_cleaner(content)
	for i in content.split():
		add_to_index(index,url,i)

def my_page_cleaner(page_content): #A robust function which uses beautiful soup for extracting text
	soup = BeautifulSoup(page_content)

	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract()  # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)

	# print(text)
	return text

def compute_ranks(graph): #Computing ranks for a given graph -> for all the links in it
	d=0.8
	numloops=10
	ranks={}
	npages=len(graph)
	for page in graph:
		ranks[page]=1.0/npages
	for i in range(0,numloops):
		newranks={}
		for page in graph:
			newrank=(1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank=newrank+d*ranks[node]/len(graph[node])
			newranks[page]=newrank
		ranks=newranks
	return ranks
	
def Crawl_web(seed):#The website to act as seed page is given as input
	tocrawl=[seed]
	crawled=[]
	index={}
	graph={}#new graph
	global max_limit
	depth = max_limit
	counter = 0
	while len(tocrawl) > 0 :
		p=tocrawl.pop()
		# print "Counter = "+str(counter)
		print "Current size = "+str(len(tocrawl))
		print "Current page = "+str(p)
		if p not in crawled:#To remove the looping, if a page is already crawled and it is backlinked again by someother link we are crawling, we need not crawl it again
			# max_limit-=1
			# print max_limit
			# if max_limit<=0:
			# 	break
			c=get_page(p)
			add_page_to_index(index,p,c)
			f=get_all_links(c)
			crawled.append(p)#As soon as a link is crawled it is appended to crawled. In the end when all the links are over, we will return the crawled since it contains all the links we have so far
			crawled, index, graph = Crawl_web2(depth - 1 , f, crawled, index, graph)
			# print "f = "+str(f)
			# tocrawl = union(tocrawl,f)
			graph[p]=f
			counter+=1
	return crawled,index,graph #the list of links

def Crawl_web2(depth, f, crawled, index, graph):#The website to act as seed page is given as input
	if depth >= 0:
		counter = 0
		while len(f) > 0:
			p=f.pop()
			# print "Counter = "+str(counter)
			print "Current size = "+str(len(f))
			print "Current page = "+str(p)
			if p not in crawled:#To remove the looping, if a page is already crawled and it is backlinked again by someother link we are crawling, we need not crawl it again
				# max_limit-=1
				# print max_limit
				# if max_limit<=0:
				# 	break
				c=get_page(p)
				add_page_to_index(index,p,c)
				next_links = get_all_links(c)
				# print "f = "+str(next_links)
				# f = union(f,next_links)
				graph[p] = next_links
				crawled.append(p)#As soon as a link is crawled it is appended to crawled. In the end when all the links are over, we will return the crawled since it contains all the links we have so far
				# counter+=1
				crawled, index, graph = Crawl_web2(depth - 1, next_links, crawled, index, graph)
	return crawled,index,graph #Returns the list of links

def QuickSort(pages,ranks):#Sorting in descending order
	if len(pages)>1:
		piv=ranks[pages[0]]
		i=1
		j=1
		for j in range(1,len(pages)):
			if ranks[pages[j]]>piv:
				pages[i],pages[j]=pages[j],pages[i]
				i+=1
		pages[i-1],pages[0]=pages[0],pages[i-1]
		QuickSort(pages[1:i],ranks)
		QuickSort(pages[i+1:len(pages)],ranks)

def Look_up_new(index,ranks,keyword):
	pages=Look_up(index,keyword)
	print '\nPrinting the results as is with page rank\n'
	for i in pages:
		print i+" --> "+str(ranks[i])#Displaying the lists, so that you can see the page rank along side
	QuickSort(pages,ranks)
	print "\nAfter Sorting the results by page rank\n"
	it=0
	for i in pages:#This is how actually it looks like in search engine results - > sorted by page rank
		it+=1
		print str(it)+'.\t'+i+'\t'+str(keyword)+'\n'


#print index
print "Enter the seed page"
seed_page=raw_input()
print "Enter What you want to search"
search_term=raw_input()
try:
	print "Enter the depth you wanna go"
	max_limit=int(raw_input())
except:
	f=None
print '\nStarted crawling, presently at depth..'
crawled,index,graph=Crawl_web(seed_page)#printing all the links

ranks=compute_ranks(graph)#Calculating the page ranks
searches = search_term.split();
for i in searches:
	Look_up_new(index,ranks,i)