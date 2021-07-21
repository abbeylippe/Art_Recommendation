# program chooses a random avant-garde or postmodern artist from a list on wikipedia

# future ideas:
# people can enter a genre and randomly recommends an artist
# people can enter an artist(s) and it will recommend a similar one (based on genre)

import requests
from bs4 import BeautifulSoup
import re
import random
import tkinter as tk

from requests.api import post

impressionism = "impressionism"
avantGarde = "avant-garde"
postmodern = "postmodern"

def processNames(artist_lists, names, option):
    index = 0
    for artist_list in artist_lists:

        if (option == impressionism and index == 1): # the elements reside within a paragraph
            text = []
            artist_list = artist_list.find_all('a') # process to get them into list form
            for artist in artist_list:
                text.append(artist.text)


        else: 
            text = artist_list.text
            # split the text according to newline to create an array of names
            text = text.split("\n")

        # pattern to match up until an opening bracket to extract just the names
        match = "^[^\(]+"
        r1 = re.compile(match)

        for name in text:
            if (name[0].isalpha() == False):
                continue
            # also removes commas
            name = name.split(',')
            x = r1.search(name[0])
            # remove trailing white spaces
            names.add(x.group().rstrip(" "))
        
        index+=1

def handleSearchPress():
    genre = entry.get() # returns the text entered into the entry box

    if (genre == "avant-garde" or genre == "avant garde" or genre == "modernism" or genre == "modernist"):
        option = avantGarde
        URL = "https://en.wikipedia.org/wiki/List_of_avant-garde_artists"

    elif (genre == 'postmodernism' or genre == "contemporary" or genre == "postmodern"):
        option = postmodern
        URL = "https://en.wikipedia.org/wiki/List_of_contemporary_artists"
    
    elif (genre == "impressionism" or genre == "impressionist"):
        option = impressionism
        URL = "https://en.wikipedia.org/wiki/Impressionism"
    
    else: # genre is unrecognised
        answer['text'] = "genre not recognised, try again"
        return

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # id that the names are in 
    content = soup.find(id="mw-content-text")
    artist_lists = []

    if (option == avantGarde):
        # list is the second ul of the section
        containing = content.find_all("ul", limit=2)
        artists = containing[1]
        artist_lists.append(artists)
    elif (option == postmodern):
        # 26 lists start with the 3rd list (split alphabetically)
        containing = content.find_all("ul", limit=28)
        artists = containing[2:]
        for artist in artists:
            artist_lists.append(artist)
    elif(option == impressionism):
        # list is in the 3rd ul of the section
        containing = content.find_all("ul", limit=3)
        artists = containing[2] 
        artist_lists.append(artists)
        #print(artists)
        womenHeader = soup.find(id="Women_Impressionists").find_parent('h2')
        paragraphs = womenHeader.find_next_siblings('p')
        artist_lists.append(paragraphs[1]) # names reside in the second paragraph

    names = set() # ensure the same name isn't added twice

    processNames(artist_lists, names, option)

    lst = list(names) # allow for random.choice to be called
    name = random.choice(lst)
    answer["text"] = name


window = tk.Tk()
window.title("Art Recommendation")
window.config(bg="white")
window.iconbitmap('heart.ico')


button_frame = tk.Frame()
greeting_frame = tk.Frame()
entry_frame = tk.Frame()
answer_frame = tk.Frame()
greeting = tk.Label(text="Choose an art movement", master=greeting_frame, font=("Bookman", 15, 'bold'), bg="white", fg="#800000")
entry = tk.Entry(master=entry_frame)
button = tk.Button(text="Search", master=button_frame, command=handleSearchPress, font=("Bookman", 10), fg="#800000")
answer = tk.Label(text="", master=answer_frame, bg="white") # need to update this with some text...


greeting.pack()
entry.pack()
button.pack()
answer.pack()

greeting_frame.pack(fill=tk.Y, expand=True, pady=20, padx=20)
entry_frame.pack(fill=tk.Y, expand=True, padx=20, pady=(10, 5))
button_frame.pack(fill=tk.Y, expand=True, pady=(0, 20))
answer_frame.pack(fill=tk.Y, expand=True, pady=(0, 10))

window.mainloop()




