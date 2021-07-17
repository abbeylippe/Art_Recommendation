# program chooses a random avant-garde artist from a list on wikipedia

# people can enter a genre and randomly recommends an artist
# people can enter an artist(s) and it will recommend a similar one (based on genre)

import requests
from bs4 import BeautifulSoup
import re
import random

def processNames(artist_list, names):
    text = artist_list.text
    # split the text according to newline to create an array of names
    text = text.split("\n")

    # pattern to match up until an opening bracket to extract just the names
    match = "^[^\(]+"
    r1 = re.compile(match)

    for name in text:
        # also removes commas
        name = name.split(',')
        x = r1.search(name[0])
        # remove trailing white spaces
        names.append(x.group().rstrip(" "))

genre = input("Enter the genre you want to explore: ")
print(genre)


if (genre == "avant-garde" or genre == "avant garde" or genre == "modernism"):
    option = "avant-garde"
    URL = "https://en.wikipedia.org/wiki/List_of_avant-garde_artists"

elif (genre == 'postmodernism' or genre == "contemporary" or genre == "postmodern"):
    option = "postmodern"
    URL = "https://en.wikipedia.org/wiki/List_of_contemporary_artists"


page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# id that the list is in 
content = soup.find(id="mw-content-text")

if (option == "avant-garde"):
    # list is the second ul of the section
    first2 = content.find_all("ul", limit=2)
    artists = first2[1]
elif (option == "postmodern"):
    # 26 lists start with the 3rd list (split alphabetically)
    first3 = content.find_all("ul", limit=28)
    artists = first3[2:]

names = []

if (option == "avant-garde"):
    processNames(artists, names)

else:
    for artist_list in artists:   
        processNames(artist_list, names)

print(random.choice(names))



