# yts-cli
A Python3 script to download [YTS](https://yts.mx) movies with the help of [transmission-gtk](https://transmissionbt.com) torrent client.


# Usage
Usage : `./yts [-h] [-f MOVIE YEAR] [-d MOVIE YEAR FORMAT] [-s MOVIE] [-p]`


**Note**: Only one flag is to be used at a time.

Flags:
```
 -h, --help                       # show this help message and exit
 -f (formats) MOVIE YEAR          # shows the available movie formats
 -d (download) MOVIE YEAR FORMAT  # downloads movie torrent in the given format
 -s (search) MOVIE                # search movies in yts
 -p (popular)                     # shows popular downloads
```

Example :
```
$ ./yts -p
$ ./yts -f the-nun 2018
$ ./yts -d the-nun 2018 1080p.WEB
$ ./yts -s nun  
```
