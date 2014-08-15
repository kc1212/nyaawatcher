
# a wget example
# wget -d --header "Host: www.nyaa.se" --header "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0" --header "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" --header "Accept-Language: en-gb,en;q=0.5" --header "Referer: http://www.nyaa.se/?page=view&tid=587070" --header "Connection: keep-alive" "http://www.nyaa.se/?page=download&tid=587070" -O myfile.torrent

import urllib.request
import urllib.parse
import urllib.error
import time
import re # regex

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

    # TODO need to check second element is a number
    # TODO use csv library
    f = open(filename, "r")
    wlist = [tuple(i.rstrip().split(",")) for i in f.readlines()]
    f.close()
    return wlist


def search_torrent(wlist):

    download_val = []
    for x,y in wlist:
        x = x.replace(" ", "+")
        x = x.replace("%EPS", y)
        search_vals = SEARCH_VAL
        search_vals['term'] = x
        search_url = NYAA + "?" + urllib.parse.urlencode(search_vals)
        req = urllib.request.Request(search_url)

        try:
            response = urllib.request.urlopen(req)
            if response.url.find("page=view&tid") is not -1:
                results = response.read().decode("utf-8")
                m = re.search("page=download&#38;tid=\d+", results).group(0)
                m = m.replace("#38;", "")
                download_val.append(m)
            elif response.url.find("page=search") is not -1:
                print(x + " is not found or has no unique results")
            else:
                print(x + " unknown error")
                print("\t" + response.url)

        except Exception as e:
            print(e.reason)
            print(e.message)

    return download_val


def download_torrent(download_val):

    count = 0 # number of downloaded file
    for x in download_val:
        download_url = NYAA + "?" + x
        req = urllib.request.Request(download_url, headers = DOWNLOAD_HEADER)

        try:
            response = urllib.request.urlopen(req)
            filename = re.search('".*"', response.getheader("Content-Disposition")).group(0)[1:-1]
            save_torrent_file(filename, response.read())
            count += 1
            print("saved " + filename)

        except Exception as e:
            print(e.reason)
            print(e.message)

    return count


if __name__ == "__main__":

    wlist = parse_watchlist("watchlist.txt")
    download_val = search_torrent(wlist)
    ret = download_torrent(download_val)

    print("downloaded " + str(ret) + " file(s).")


