# -*- coding: utf-8 -*-

#The schedule of animeNfo radio

#Standard modules
import sys, os, datetime

#External modules
import requests
from bs4 import BeautifulSoup


def show_help():

    print("If you input no option, you can get information of the current song and the block and the five coming up songs.\n ")
    print("--current  You can check about only current information")
    print("--help     Show the available options")


#Clear the terminal screen
def cls():

    #For windows
    if os.name == "nt":
        command = "cls"

    #For Other os 
    else:
        command = "clear"

    os.system(command)
    

#Color text with ANSI escape sequense 
def color(song_data):

    if os.name == "nt":
        #Do nothing because ANSI escape sequense is not available in windows
        return song_data

    red = "\033[31m"
    default = "\033[0m" #default text color
    song_data[0] = red + song_data [0] + default

    return song_data


#Delete some tags and special charactors in title and artist information
def form_data(data):
    
    to_delete = ['\"', "href", "amp",] 

    for string in to_delete:
        data = data.replace(string, "")

    return data


#Delete some tags and special charactors in series information
def form_series_data(series):

    to_delete = ['<div class="span2 seriestag"', "</div>", "\n", \
                "\t", ">", "href", "\xa0", "amp"]
    
    for string in to_delete:
        series = series.replace(string, "")

    return series


def display_coming_up(source):

    schedule= source.find_all(class_="span5")
    raw_series_list = source.find_all(class_="span2 seriestag")

    schedule.pop(0)
    
    songs = []

    for song in schedule:
        splited_data = str(song).split("=")
        songs.append(splited_data[3])

    artist_list = []
    title_list = []

    for song in songs:

        splited_song = song.split(" - ")

        artist = form_data(splited_song[0])

        title = form_data(splited_song[1])
        
        artist_list.append(artist)
        title_list.append(title)


    series_list = []

    for series in raw_series_list:
        series = form_series_data(str(series))
        series_list.append(series)
    
    print("")
    print("Coming up:")
    print("")
    print("Artist - Title - Series")

    #Replace with N/A if series information is not included
    series_list = [i if i != ""  else "N/A" for i in series_list]

    for artist, title, series in zip(artist_list, title_list, series_list):

        print(f"{artist} - {title} - {series}")


def main(no_coming_up):

    cls()
    
    try:
        res = requests.get("https://www.animenfo.com/radio/nowplaying.php", timeout=6)

    except Exception:
        print("Connection Error!")
        sys.exit()

    if res.status_code != 200:
        print("Connection Error!")
        sys.exit()

    source = BeautifulSoup(res.text, "lxml")
    schedule = source.find(id="schedule_container").get_text()

    schedule = schedule.splitlines()

    #Remove needless elements
    schedule.pop(2)
    schedule.pop(4)
    schedule.pop(1)
    schedule.pop(0)

    print("Currently on schedule:")

    for element in schedule:
        print(element)

    print("")
    print("Now playing:")

    song_data = source.find(class_="span6").get_text().splitlines()

    artist_place = 1
    artist = color(song_data[artist_place].split(":"))

    #If "Circle(s)/Group(s)" information contain in currently song, shift the data place
    if song_data[2][0] == "C": 
        title_place = 3
        series_place = 6

    else:
        title_place = 2
        series_place = 5

    title = color(song_data[title_place].split(":"))
    series = color(song_data[series_place].split(":"))


    song_data[1] = ":".join(artist)
    song_data[title_place] = ":".join(title)
    song_data[series_place] = ":".join(series)

    for data in song_data:
        print(data)

    if no_coming_up:
        sys.exit()

    else:
        display_coming_up(source)


if __name__ == "__main__":

    argv = sys.argv
    length = len(argv)

    if length == 1:
        #No option: Current information and coming up songs will be displayed
        no_coming_up = False

    elif argv[1] == "--current":
        #Coming up songs information won't be displayed
        no_coming_up = True 

    elif argv[1] == "--help":
        show_help()
        sys.exit()

    else:
        #Error
        print("Option error")
        print('You can check the options by "--help" option')
        sys.exit()

    main(no_coming_up)
