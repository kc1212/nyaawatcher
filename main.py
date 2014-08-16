#!/bin/python3

# a wget example
# wget -d --header "Host: www.nyaa.se" --header "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0" --header "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" --header "Accept-Language: en-gb,en;q=0.5" --header "Referer: http://www.nyaa.se/?page=view&tid=587070" --header "Connection: keep-alive" "http://www.nyaa.se/?page=download&tid=587070" -O myfile.torrent

"""
example usage:
    watch -n 120 ./main.py
"""

import urllib.request
import urllib.parse
import urllib.error
import csv
import time
import re # regex
import os


NYAA="http://www.nyaa.se/"
SEARCH_VAL = { "page":"search", "cats":"0_0", "filter":"0", }
DOWNLOAD_HEADER = {
 "Host": "www.nyaa.se",
 # "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 "Accept-Language": "en-gb,en;q=0.5",
 # "Accept-Encoding": "gzip, deflate",
 # "Referer": "http://www.nyaa.se/?page=view&tid=587678",
 "Connection": "keep-alive"
}


def save_torrent_file(filename, data):

    f = open(filename, "wb+")
    f.write(data)
    f.close()


def parse_watchlist(filename):

    wlist = []
    count = 0

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            wlist.append((row[0], int(row[1]), len(row[1]), count))
            count += 1
    return wlist


def search_torrent(wlist):

    download_val = []

    for term, eps, c, i in wlist:
        term = term.replace(" ", "+")
        term = term.replace("%EPS", str(eps).zfill(c))
        search_vals = SEARCH_VAL
        search_vals['term'] = term
        search_url = NYAA + "?" + urllib.parse.urlencode(search_vals)
        req = urllib.request.Request(search_url)

        try:
            response = urllib.request.urlopen(req)
            if response.url.find("page=view&tid") is not -1:
                results = response.read().decode("utf-8")
                m = re.search("page=download&#38;tid=\d+", results).group(0)
                m = m.replace("#38;", "")
                download_val.append((m,i)) # include the index of csv
            elif response.url.find("page=search") is not -1:
                print(term + " is not found or has no unique results")
            else:
                print(term + " unknown error")
                print("\t" + response.url)

        except Exception as e:
            print(e.reason)
            print(e.message)

    return download_val


def download_torrent(download_val):

    downloaded_list = []
    for x, i in download_val:
        download_url = NYAA + "?" + x
        req = urllib.request.Request(download_url, headers = DOWNLOAD_HEADER)

        try:
            response = urllib.request.urlopen(req)
            filename = re.search('".*"', response.getheader("Content-Disposition")).group(0)[1:-1]
            save_torrent_file(filename, response.read())
            downloaded_list.append(i)
            print("saved " + filename)

        except Exception as e:
            print(e.reason)
            print(e.message)

    return downloaded_list


def update_watchlist(wlist, ulist, filename): # ulist is list needs updating

    with open(filename+".tmp", 'w') as csvfile:
        writer = csv.writer(csvfile)
        for term, eps, c, i in wlist:
            if i in ulist:
                eps += 1
            row = [term, str(eps).zfill(c)]
            writer.writerow(row)

    os.remove(filename)
    os.rename(filename+".tmp", filename)


if __name__ == "__main__":

    filename = "watchlist.csv"

    wlist = parse_watchlist(filename)
    download_val = search_torrent(wlist)
    ret = download_torrent(download_val)

    if len(ret) is not 0:
        update_watchlist(wlist, ret, filename)

    print("downloaded " + str(len(ret)) + " file(s).")





