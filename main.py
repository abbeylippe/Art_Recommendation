# program chooses a random avant-garde artist from a list on wikipedia

import requests
from bs4 import BeautifulSoup
import re
import random

URL = "https://en.wikipedia.org/wiki/List_of_avant-garde_artists"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# id that the list is in 
content = soup.find(id="mw-content-text")

# the list is in the second ul of the section
first2 = content.find_all("ul", limit=2)
artists = first2[1]
text = artists.text
# split the text according to whitespace to create an array of names
text = text.split("\n")

# pattern to match up until an opening bracket to extract just the names
r1 = re.compile("^[^\(]+")

names = []

for name in text:
    x = r1.search(name)
    # remove trailing white spaces
    names.append(x.group().rstrip())

print(random.choice(names))


