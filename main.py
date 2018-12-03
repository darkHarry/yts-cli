#! /usr/bin/python3

import requests
import bs4
import sys
import os

def print_usage():
    print("Usage: ./main.py <movie-name> <year>")
    print("Example: \"./main.py the-nun 2018\"")
    print("Example: \"./main.py the-nun 2018 1080p.WEB\"")
    exit()

def get_movie_details():
    movie_name = None
    movie_format = None
    if len(sys.argv) == 3:
        movie_name = get_movie_name()
    elif len(sys.argv) == 4:
        movie_name = get_movie_name()
        movie_format = get_movie_format()
    else:
        print_usage()

    return (movie_name, movie_format)

def get_movie_name():
        return sys.argv[1].lower()+"-"+sys.argv[2]

def get_movie_format():
        return sys.argv[3]

def check_format_availability(format, formats):
    return format in formats

def get_movie_page(movie):
    link = "https://yts.am/movie/"+movie
    res = requests.get(link)
    if res.status_code == requests.codes.ok:
        return res

def extract_formats(movie_page):
    movie_formats = bs4.BeautifulSoup(movie_page.text, "lxml").select("p[class='hidden-xs hidden-sm']")[0].find_all("a")
    links = {}
    for movie_format in movie_formats:
        links[movie_format.getText()] = movie_format["href"]
    return links

def print_formats(formats):
    print("Available In:")
    for key in formats.keys():
        print("\t", key)
 

def get_torrent(movie_name, torrent_link):
    res = requests.get(torrent_link)
    if res.status_code == requests.codes.ok:
        if os.path.isfile(movie_name+".torrent"):
            print("Torrent file exists")
        else:
            open(movie_name+".torrent", "wb").write(res.content)

if __name__ == "__main__":
    movie_name, movie_format = get_movie_details() 
    if not movie_name:
        exit()
    
    movie_page = get_movie_page(movie_name)
    if not movie_page:
        print("Movie Page does not exist!")    

    formats = extract_formats(movie_page)
    if not formats:
        print("Cannot get movie formats")
    
    if movie_format:
        if check_format_availability(movie_format, formats):
            torrent_link = formats[movie_format]
            get_torrent(movie_name, torrent_link)
        else:
            print("{} format not available for {}".format(movie_format, movie_name))
    else: 
        print_formats(formats)
