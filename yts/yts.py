#! /usr/bin/env python3
# yts

import requests
import argparse
import bs4
import sys
import os
import subprocess


# Make request to the given url
# Returns the response object
# TODO give a user-friendly error
def make_request(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit()

    return res


# YTS CLASS
class YTS:
    """ provides an API for downloading yts yifi movies. """

    # Initialize with the current yts url
    def __init__(self, yts_url):
        self.url = yts_url

    # Gets the popular downloads from the homepage
    # Returns a dictionary with movie title and rating
    def get_popular_downloads(self) -> dict:
        res = make_request(self.url)
        pop_movies_dict = {}
        pop_movies = (
            bs4.BeautifulSoup(res.text, "lxml")
            .select("#popular-downloads")[0]
            .select("div[class='browse-movie-wrap col-xs-10 col-sm-5']")
        )
        for movie in pop_movies:
            movie_data = movie.select("a")[0]
            pop_movies_dict.update(self.extract_movie_data(movie_data))
        return pop_movies_dict

    # Gets the search result for the query
    # Returns a dictionary with movie title and rating
    def search_movies(self, query):
        url = f"{self.url}browse-movies/{query}"
        res = make_request(url)
        query_dict = {}
        movies_found = (
            bs4.BeautifulSoup(res.text, "lxml")
            .select("section > div[class='row']")[0]
            .select("div[class='browse-movie-wrap col-xs-10 col-sm-4"
                    " col-md-5 col-lg-4']")
        )
        for movie in movies_found:
            movie_data = movie.select("a")[0]
            query_dict.update(self.extract_movie_data(movie_data))
        return query_dict

    # Gets the movie available formats
    # Returns a dictionary with formats and torrent-url
    def get_movie_formats(self, movie_title):
        movie_page_url = self.url+"movies/"+movie_title
        movie_page = make_request(movie_page_url)
        formats = self.extract_formats(movie_page)
        return formats

    # STATIC FUNCTIONS #

    # Get the movie formats from the movie page
    # Returns a dictionary of formats with their torrent urls as values
    @staticmethod
    def extract_formats(movie_page) -> dict:
        movie_formats = (
            bs4.BeautifulSoup(movie_page.text, "lxml")
            .select("p[class='hidden-xs hidden-sm']")[0]
            .find_all("a")
        )
        torrent_urls = {}
        for movie_format in movie_formats:
            torrent_urls[movie_format.getText()] = movie_format["href"]
        return torrent_urls

    # Download and save movie torrent file to current folder
    # Returns torrent name (eg: the-nun-2018.torrent)
    @staticmethod
    def get_torrent(movie_title, torrent_url):
        res = make_request(torrent_url)
        torrent_name = movie_title + ".torrent"
        if not os.path.isfile(torrent_name):
            with open(torrent_name, "wb") as torrent_file:
                torrent_file.write(res.content)
        else:
            # TODO Tell user file already exists
            pass
        return torrent_name

    # Used by get_popular_downloads and search_movies
    # extracts movie title with its rating
    # Returns a dictionary (eg {'the-nun-2018': '5.3 / 10'})
    @staticmethod
    def extract_movie_data(movie_data) -> dict:
        movie_title = movie_data["href"].split("/")[-1]
        rating = (
            movie_data
            .select("figcaption > h4[class='rating']")[0]
            .getText()
        )
        return {movie_title: rating}

    # Execute Transmission-gtk with the downloaded torrent
    @staticmethod
    def execute_transmission(torrent_name):
        subprocess.Popen(["transmission-gtk", torrent_name])


# TODO design a better cli usage
# Handle CLI arguments Class
class Arguments:
    # Initialize arguments
    def __init__(self):
        self.arguments = self.get_cli_args()

    # Handles CLI arguments
    # Returns a dictionary of the arguments
    # Only one flag is to be applied at a time
    @staticmethod
    def get_cli_args() -> dict:
        parser = argparse.ArgumentParser(prog="yts",
                                         description=("Downloads YTS"
                                                      "movie torrents."),
                                         allow_abbrev=False)

        flags = parser.add_mutually_exclusive_group(required=True)
        # Add available movie formats argument
        flags.add_argument("-f",
                           nargs=1,
                           metavar=("MOVIE-TITLE"),
                           action="store",
                           help="shows the available movie formats")

        # Add download movie torrent argument
        flags.add_argument("-d",
                           nargs=2,
                           metavar=("MOVIE-TITLE", "FORMAT"),
                           action="store",
                           help="downloads movie torrent in the given format")

        # Add search movie argument
        flags.add_argument("-s",
                           nargs=1,
                           metavar="MOVIE-NAME",
                           action="store",
                           help="search movies in yts")

        # Add popular movies argument
        flags.add_argument("-p",
                           action="store_true",
                           help="shows popular downloads")

        # create argument dictionary
        arguments_dict = vars(parser.parse_args())
        return arguments_dict

    def __getitem__(self, arg):
        return self.arguments[arg]


def main():
    yts = YTS("https://yts.mx/")
    args = Arguments.get_cli_args()

    # Handle arguments
    if args["p"]:
        pop_movies = yts.get_popular_downloads()
        if pop_movies:
            print("Popular Downloads:")
            for movie, rating in pop_movies.items():
                print(f"\t{movie} ({rating})")

    elif args["s"]:
        results = yts.search_movies(args["s"])
        print("Movies Found:")
        for movie, rating in results.items():
            print(f"\t{movie} ({rating})")

    elif args["f"]:
        movie_title = args["f"][0]
        formats = yts.get_movie_formats(movie_title)
        print("Available In:")
        for key in formats.keys():
            print("\t", key)

    elif args["d"]:
        name, year, movie_format = args["d"]
        title, formats = yts.get_movie_data(name, year)
        if movie_format in formats:
            torrent_url = formats[movie_format]
            torrent_name = yts.get_torrent(title, torrent_url)
            if not torrent_name:
                print("Cannot download torrent")
            else:
                yts.execute_transmission(torrent_name)
        else:
            print(f"{movie_format} format not available for {name}")


if __name__ == "__main__":
    main()
