#! /usr/bin/python3

import requests
import bs4
import sys

def get_movie_name():
    if len(sys.argv) != 3:
        print("Usage: ./main.py <movie-name> <year>")
        print("Example: \"./main.py the-nun 2018\"")
        exit()
    return sys.argv[1].lower()+"-"+sys.argv[2]

def get_movie_page(movie):
    link = "https://yts.am/movie/"+movie
    res = requests.get(link)
    if res.status_code == requests.codes.ok:
        return res
    else:
        None

def get_formats(movie_page):
    movie_formats = bs4.BeautifulSoup(movie_page.text, "lxml").select("p[class='hidden-xs hidden-sm']")[0].find_all("a")
    links = {}
    for movie_format in movie_formats:
        links[movie_format.getText()] = movie_format["href"]
    return links

def get_torrent(movie_name, torrent_link):
    res = requests.get(torrent_link)
    if res.status_code == requests.codes.ok:
        open(movie_name+".torrent", "wb").write(res.content)

movie_page = get_movie_page(get_movie_name())
get_torrent(get_movie_name(), get_formats(movie_page)["720p.WEB"])

