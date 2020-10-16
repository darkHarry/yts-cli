#! /usr/bin/env python3
# yts

import requests
import argparse
import bs4
import sys
import os
import subprocess


# YTS CLASS
class YTS:
    """ provides an API for downloading yts yifi movies. """

    def __init__(self, yts_url):
        """
        Initialize with the current yts url

        Parameters
        ----------
        yts_url: str, required
            The URL of the yts website
        """

        self.url = yts_url

    def get_popular_downloads(self) -> dict:
        """
        Gets the popular downloads from the homepage
        Returns a dictionary with movie title and rating

        Returns
        -------
        pop_movies_dict: dictionary, { title(str): rating(str) }
            Dictionary with movie title and rating
            (eg {'totally-under-control-2020': '7.1 / 10'} )
        """
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

    def search_movies(self, query):
        """
        Gets the search result for the query
        Returns a dictionary with movie title and rating

        Parameters
        ----------
        query: str, required
            A name of a movie to search

        Returns
        -------
        query_dict: dictionary, { title(str): rating(str) }
            Dictionary with movie title and rating
            (eg {'totally-under-control-2020': '7.1 / 10'} )
        """
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

    def get_movie_formats(self, movie_title):
        """
        Gets the movie available formats
        Returns a dictionary with formats and torrent-url

        Parameters
        ----------
        movie_title: str, required
            A title string of a movie to get details

        Returns
        -------
        formats: dictionary, { format(str): torrent_url(str) }
            Dictionary with formats and torrent-url
            (eg {'720p.WEB': 'https://yts.mx/torrent/download/...'})
        """
        movie_page_url = self.url+"movies/"+movie_title
        movie_page = make_request(movie_page_url)
        formats = self.extract_formats(movie_page)
        return formats

    def get_torrent(self, torrent_url):
        """
        Download and return movie torrent file raw

        Parameters
        ----------
        torrent_url: str, required
            URL of the torrent file

        Returns
        -------
        res: raw, file
            The downloaded torrent file
        """
        res = make_request(torrent_url)
        return res

    # STATIC FUNCTIONS #

    @staticmethod
    def extract_formats(movie_page) -> dict:
        """
        Get the movie formats from the movie page
        Returns a dictionary of formats with their torrent urls as values

        Parameters
        ----------
        movie_page: Response, required
            Response object of the http request to the movie page

        Returns
        -------
        torrent_urls: dictionary, { format(str): torrent_url(str) }
            Dictionary of formats with their torrent urls as values
            (eg {'720p.WEB': 'https://yts.mx/torrent/download/...'})
        """
        movie_formats = (
            bs4.BeautifulSoup(movie_page.text, "lxml")
            .select("p[class='hidden-xs hidden-sm']")[0]
            .find_all("a")
        )
        torrent_urls = {}
        for movie_format in movie_formats:
            torrent_urls[movie_format.getText()] = movie_format["href"]
        return torrent_urls

    @staticmethod
    def extract_movie_data(movie_data) -> dict:
        """
        Used by get_popular_downloads and search_movies
        extracts movie title with its rating
        Returns a dictionary (eg {'the-nun-2018': '5.3 / 10'})

        Parameters
        ----------
        movie_data: bs4.element.Tag, required
            Page content of the movie from the website

        Returns
        -------
        dict: dictionary, {movie_title(str): rating(str)}
            Returns a dictionary (eg {'the-nun-2018': '5.3 / 10'})
        """
        movie_title = movie_data["href"].split("/")[-1]
        rating = (
            movie_data
            .select("figcaption > h4[class='rating']")[0]
            .getText()
        )
        return {movie_title: rating}

    @staticmethod
    def execute_transmission(torrent_name):
        """ Execute Transmission-gtk with the downloaded torrent

        Parameters
        ----------
        torrent_name: str, required
            Name of the torrent to be downloaded
        """
        subprocess.Popen(["transmission-gtk", torrent_name])


# TODO design a better cli usage
class Arguments:
    """ Handle CLI arguments Class """

    def __init__(self):
        """ Initialize arguments """
        self.arguments = self.get_cli_args()

    @staticmethod
    def get_cli_args() -> dict:
        """ Handles CLI arguments
        Returns a dictionary of the arguments
        Only one flag is to be applied at a time

        Returns
        -------
        arguments_dict: dictionary
            Dictionary of the cli arguments
        """
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


# TODO give a user-friendly error
def make_request(url):
    """ Make request to the given url
    Returns the response object

    Parameters
    ----------
    url: str, required
        target URL

    Returns
    -------
    res: response
        Returns a HTTP Response object
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit()

    return res


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
        movie_title, movie_format = args["d"]
        formats = yts.get_movie_formats(movie_title)
        if movie_format in formats:
            torrent_url = formats[movie_format]
            torrent = yts.get_torrent(torrent_url)
            torrent_name = movie_title + ".torrent"
            if not os.path.isfile(torrent_name):
                with open(torrent_name, "wb") as torrent_file:
                    torrent_file.write(torrent.content)
            else:
                print(f"{torrent_name} exists")
            YTS.execute_transmission(torrent_name)
        else:
            print(f"{movie_format} format not available for {movie_title}")


if __name__ == "__main__":
    main()
