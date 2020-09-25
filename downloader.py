import shutil
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import time
import os

# import requests

search = "girl"  # asian+pic
category = "001"  # general 100, anime 010, people 001 combine 110,101,111,001,011
purity = "110"  # Sketchy 010, SWF 100 combine 110
order = "desc"
sort = "favorites"
startPage = 1600
noOfImages = 64000
endPage = int((noOfImages / 24) + 8)
pageImg = 1
count = 1
database_file = "img_names.txt"
img_folder = "./images"

url = (
    "https://wallhaven.cc/search?q="
    + search
    + "&categories="
    + category
    + "&purity="
    + purity
    + "&topRange=1M&sorting="
    + sort
    + "&order="
    + order
    + "&page="
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
}


def find_name_in_file(filename, name_to_find):
    result = False
    f = open("img_names.txt", "r")
    # Wlaking top-down from the root
    contents = f.read().split()
    for filename in contents:
        if filename == name_to_find:
            result = True
    f.close()
    return result


def find_files_and_wirte_to_txt(search_path, filename):
    f = open(filename, "a+")
    # Wlaking top-down from the rootf
    for root, dir, files in os.walk(search_path):
        for file in files:
            if not find_name_in_file(filename, file):
                f.write("%s\n" % file)
    f.close()


# initialize the session
session = HTMLSession()


for page in range(startPage, endPage):
    # time.sleep(1)
    pageImg = 1

    response = session.get(url + str(page))
    if response.status_code == 200:
        # execute Javascript
        # response.html.render(timeout=200000)

        # construct the soup parser
        soup = bs(response.html.html, "html.parser")
        try:
            for link in soup("a", "preview", href=True):
                u = link["href"].split("/")[-1]
                mainUrl = (
                    "https://w.wallhaven.cc/full/" + u[:2] + "/wallhaven-" + u + ".jpg"
                )
                print(
                    mainUrl
                    + "  page-"
                    + str(page)
                    + " img-"
                    + str(pageImg)
                    + " totImg-"
                    + str(count)
                )
                count += 1
                pageImg += 1

                if not find_name_in_file(database_file, u + ".jpg"):
                    print("not Found in DB Downloading...")
                    response = session.get(mainUrl, stream=True)
                    print("Downloaded")
                    if response.status_code == 200:
                        with open(img_folder + "/" + u + ".jpg", "wb") as out_file:
                            shutil.copyfileobj(response.raw, out_file)
                        f = open(database_file, "a+")
                        f.write(u + ".jpg" + "\n")
                        f.close()
                    try:
                        del response
                    except:
                        pass
        except Exception as e:
            print("Error - Data Scraping Failed " + url + str(page) + " {}".format(e))
    else:
        print(url + str(page))
        print(
            "Site is not responding or internet is not availabe {}".format(
                response.status_code
            )
        )
    try:
        del response
    except:
        pass
