
# a wget example
# wget -d --header "Host: www.nyaa.se" --header "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0" --header "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" --header "Accept-Language: en-gb,en;q=0.5" --header "Referer: http://www.nyaa.se/?page=view&tid=587070" --header "Connection: keep-alive" "http://www.nyaa.se/?page=download&tid=587070" -O myfile.torrent

import urllib.request
import urllib.parse
import urllib.error
import re # regex

NYAA="http://www.nyaa.se/"
SEARCH_VAL = { "page":"search", "cats":"0_0", "filter":"0", }

# TODO need to check second element is a number
f = open("watchlist.txt", "r")
wlist = [tuple(i.rstrip().split(";")) for i in f.readlines()]
print(wlist)
f.close()

# perform search
download_val = []

for x,y in wlist:
    x = x.replace(" ", "+")
    x = x.replace("%EPS", y)
    search_vals = SEARCH_VAL
    search_vals['term'] = x
    search_url = NYAA + "?" + urllib.parse.urlencode(search_vals)
    req = urllib.request.Request(search_url)

    try: response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        print(e.reason)

    # check response
    if response.url.find("page=view&tid") != -1:
        results = response.read().decode("utf-8")
        m = re.search("page=download&#38;tid=\d+", results).group(0)
        m = m.replace("#38;", "")
        download_val.append(m)

print(download_val)

# req = urllib.request.Request(
# for query in


