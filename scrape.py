#a program to scrape info from Craigslist
#@ColeHanson

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import webbrowser
from time import sleep

class Listing:

    type = 'listing'

    def __init__(self, name,price,location, link, priority = 0 ):
        self.name = name
        self.price = price
        self.location = location
        self.link = link
        self.priority = 0

    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def setPrice(self,cost):
        self.price = cost
    def getLocation(self):
        return self.location
    def getLink(self):
        return self.link
    def setPriority(self, num):
        self.priority = num
    def getPriority(self):
        return self.priority

def parse_page(URL):
    '''
    parses URL for info on listings, extracts proper data
    '''

    #connect to URL, read page, close
    uClient = uReq(URL)
    pageHTML = uClient.read()
    uClient.close()

    #create a soup with html parser
    soupPage = soup(pageHTML, "html.parser")

    # grabs results,prices and info from a given craigslist page
    results = soupPage.findAll('li', {'class':'result-row'} )
    listings = []

    prices = []
    locations = []
    titles = []
    links = []
    dates = soupPage.findAll('time', {'class':'result-date'} )
    count = 1
    for i in results:
        price = i.find('span', {'class':'result-price'} )
        location = i.find('span', {'class':'result-hood'})
        title = i.find('a', {'class': 'result-title'})
        link = i.a['href']

        # catch for null elements
        if price is None:
            pass
        elif location is None:
            pass
        elif location is None:
            pass
        elif title is None:
            pass

        else:
            #get the data from the parsed html
            curListPrice = price.contents[0]
            curListLocation = location.contents[0]
            curListTitle = title.contents[0]

            #create unique listing pbject
            listing = count
            listing = Listing(curListTitle,curListPrice,curListLocation,link)
            listings.append(listing)
            print("----------------------------")
            print (listing.getName())
            print (listing.getPrice())
            print (listing.getLocation())
            print (listing.getLink())
            print("----------------------------")
            print("                                                       ")
            #add elements to lists, update count
            prices.append(curListPrice)
            locations.append(curListLocation)
            titles.append(curListTitle)
            links.append(link)
            count = count + 1

    return listings

def search_Listings(search_key, listings):
    search_key = search_key.lower()
    global key_words
    key_words = search_key.split(" ")
    matches = []
    for word in key_words:
        for listing in listings:
            if word in (listing.getName().lower()):
                possible_matches.append(listing)

def prioritize():
    for match in possible_matches:
        price = int((match.getPrice())[1:])
        match.setPrice(price)



def main():
    # a list of possible cndidates based on search key
    global possible_matches
    possible_matches = []

    search_key = input("what would you like to look for? (Please be concise and descriptive)-->")

    # Craigslist chicago furniture
    URL = 'https://minneapolis.craigslist.org/d/electronics/search/ela'
    listings = parse_page(URL)
    search_Listings(search_key, listings)
    next_pages = URL + '?s='
    curNum = 120
    for i in range(0,24):
        URL = next_pages + str(curNum)
        curNum = curNum + 120
        listings = parse_page(URL)
        search_Listings(search_key, listings)

    print(len(possible_matches))

    webbrowser.open('https://minneapolis.craigslist.org/d/electronics/search/ela')

    for i in possible_matches:
        print("$$$$$$$$$$$$$$$$$$$$$$")
        print (i.getName())
        print (i.getPrice())
        print (i.getLocation())
        print (i.getLink())
        print("$$$$$$$$$$$$$$$$$$$$$$")
        print("                                                       ")

    for i in possible_matches:
        webbrowser.open_new_tab(i.getLink())
        sleep(5)


    print("Number of Matches" + len(possible_matches))

if __name__ == "__main__":
    main()
