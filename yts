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

    # Initialize with the current yts url
    def __init__(self, yts_url):
        self.url = yts_url

    # Gets the movie title from the arguments
    # Returns a string (eg: the-nun-2018)
    def get_movie_title(self, movie_name, movie_year) -> str:
        name = movie_name.lower().split()
        year = movie_year # TODO check if valid year
        return "-".join(name) + "-" + year

    # Get the movie page from movie_title
    # Returns a response object
    def get_movie_page(self, movie_title):
        url = self.url+"movie/"+movie_title
        movie_page = self.make_request(url)
        return movie_page

    # Get the movie formats from the movie page
    # Returns a dictionary of formats with their torrent urls as values
    def extract_formats(self, movie_page) -> dict:
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
    def get_torrent(self, movie_title, torrent_url):
        res = self.make_request(torrent_url)
        torrent_name = movie_title+".torrent"
        if not os.path.isfile(torrent_name):
            with open(torrent_name, "wb") as torrent_file:
                torrent_file.write(res.content)
        else:
            # TODO Tell user file already exists
            pass
        return torrent_name

    # Gets the popular downloads from the homepage
    # Returns a dictionary with movie title and rating
    def get_popluar_downloads(self) -> dict:
        res = self.make_request(self.url)
        pop_movies_dict = {}
        pop_movies = (
            bs4.BeautifulSoup(res.text, "lxml")
            .select("#popular-downloads")[0]
            .select("div[class='browse-movie-wrap col-xs-10 col-sm-5']")
        )
        for movie in pop_movies:
            movie_data = movie.select("a > figure")[0]
            pop_movies_dict.update(self.extract_movie_data(movie_data))
        return pop_movies_dict

    # Gets the search result for the query
    # Returns a dictionary with movie title and rating
    def search_movies(self, query):
        url = f"{self.url}browse-movies/{query}/all/all/0/latest"
        res = self.make_request(url)
        query_dict = {}
        movies_found = (
            bs4.BeautifulSoup(res.text, "lxml")
            .select("section > div[class='row']")[0]
            .select("div[class='browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4']")
        )
        for movie in movies_found:
            movie_data = movie.select("a > figure")[0]
            query_dict.update(self.extract_movie_data(movie_data))
        return query_dict


    ### UTIL FUNCTIONS ###

    # Make request to the given url
    # Returns the response object
    # TODO give a user-friendly error
    def make_request(self, url):
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
            sys.exit()

        return res

    # Check if argument format is present in extracted formats
    def check_format_availability(self, format, formats) -> bool:
        return format in formats

    # Used by get_popular_downloads and search_movies
    # extracts movie title with its rating
    # Returns a dictionary (eg {'the-nun (2018)': '5.3 / 10'})
    def extract_movie_data(self, movie_data) -> dict:
        movie_title = (
            movie_data
            .select("img")[0]["alt"]
            .replace("download", "")
            .strip()
        )
        rating = (
            movie_data
            .select("figcaption > h4[class='rating']")[0]
            .getText()
        )
        return {movie_title: rating}

    # Execute Transmission-gtk with the downloaded torrent
    def execute_transmission(self, torrent_name):
        command = f"transmission-gtk {torrent_name}"
        command_list = command.split()
        subprocess.Popen(command_list)

    # Utitility method to print available formats
    # Param: return of extract_format method
    def print_formats(self, formats):
        print("Available In:")
        for key in formats.keys():
            print("\t", key)


# TODO design a better cli usage
# Handle CLI arguments Class
class Arguments:

    # Initialize arguments
    def __init__(self):
        self.arguments = self.get_cli_args()
        self.check_one_flag_usage()

    # Handles CLI arguments
    # Returns a dictionary of the arguments
    # Only one flag is to be applied at a time
    def get_cli_args(self) -> dict:
        parser = argparse.ArgumentParser(prog="yts",
                                         description="Downloads YTS movie torrents.",
                                         allow_abbrev=False)

        # Add available movie formats argument
        parser.add_argument("-f",
                            nargs=2,
                            metavar=("MOVIE", "YEAR"),
                            action="store",
                            help="shows the available movie formats")

        # Add download movie torrent argument
        parser.add_argument("-d",
                            nargs=3,
                            metavar=("MOVIE", "YEAR", "FORMAT"),
                            action="store",
                            help="downloads movie torrent in the given format")

        # Add search movie argument
        parser.add_argument("-s",
                            nargs=1,
                            metavar="MOVIE",
                            action="store",
                            help="search movies in yts")

        # Add popular movies argument
        parser.add_argument("-p",
                            action="store_true",
                            help="shows popular downloads")

        # create argument dictionary
        arguments_dict = vars(parser.parse_args())
        return arguments_dict

    # Get -s search query argument
    # Returns a string
    def get_search_arguments(self) -> str:
        if self.arguments["s"] == None:
            sys.exit("Provide a search query")
        return self.arguments["s"]

    # Get -f arguments
    # Returns a list of (movie-name, year)
    def get_format_arguments(self) -> list:
        if self.arguments["f"] == None:
            sys.exit("Use the -f flag")
        elif len(self.arguments["f"]) != 2:
            sys.exit("Provide a Movie name and year")
        return self.arguments["f"]

    # Get -d arguments
    # Returns a list of (movie-name, year, format)
    def get_download_arguments(self) -> list:
        if self.arguments["d"] == None:
            sys.exit("Use the -d flag")
        elif len(self.arguments["d"]) != 3:
            sys.exit("Provide a Movie name, year and format")
        return self.arguments["d"]

    # Check for only one flag usage
    def check_one_flag_usage(self) -> None:
        flags_applied = self.number_of_flags(self.arguments)

        # create an error and exit
        if flags_applied == 0:
            sys.exit("Error: Check Usage using -h")
        elif flags_applied > 1:
            sys.exit("Error: Only one flag is applicable")

    # Returns an int of number of flags set
    def number_of_flags(self, arguments_dict) -> int:
        # Convert arguments to 0 if not present or False
        # and to 1 if present or True
        arguments_dict_int = []
        for value in arguments_dict.values():
            if value in (False, None):
                arguments_dict_int.append(0)
            else:
                arguments_dict_int.append(1)

        return sum(arguments_dict_int)


def main():
    yts = YTS("https://yts.mx/")
    args = Arguments()

    # Handle arguments
    if args.arguments["p"]:
        pop_movies = yts.get_popluar_downloads()
        if pop_movies:
            print("Popular Downloads:")
            for movie, rating in pop_movies.items():
                print(f"\t{movie} {rating}")

    elif args.arguments["s"]:
        query = args.get_search_arguments()
        search_query_res = yts.search_movies(query)
        print("Movies Found:")
        for movie, rating in search_query_res.items():
            print(f"\t{movie} {rating}")
    elif args.arguments["f"]:
        name, year = args.get_format_arguments()
        title = yts.get_movie_title(name, year)
        page = yts.get_movie_page(title)
        formats = yts.extract_formats(page)
        yts.print_formats(formats)
    elif args.arguments["d"]:
        name, year, movie_format = args.get_download_arguments()
        title = yts.get_movie_title(name, year)
        page = yts.get_movie_page(title)
        formats = yts.extract_formats(page)
        if yts.check_format_availability(movie_format, formats):
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
