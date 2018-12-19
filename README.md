# yts-cli
A Python3 script to download [YTS](https://yts.am) movies with the help of [transmission-gtk](https://transmissionbt.com) torrent client.


# Usage
Usage : `./yts [-s, --search <QUERY>] <movie-name> <year> [<format>]`

Example :
```sh
$ ./yts the-nun 2018              # shows the available formats
$ ./yts the-nun 2018 1080p.WEB    # downloads movie in the given format
$ ./yts --search nun              # shows results of search query
