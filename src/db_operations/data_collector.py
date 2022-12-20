import re
import json
import requests
import shutil
from bs4 import BeautifulSoup
import time


root_url = "https://en.wikipedia.org/wiki/List_of_Malayalam_films_of_"
start_year, end_year = 1960, 2022
ignore_list = ['BlackBerry']

movie_db = {}
for year in range(start_year, end_year+1):
    year_url = root_url + str(year)
    print(year_url)

    response = requests.get(url=year_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find("div", {"class": "mw-parser-output"})
    tables = div.find_all("table", {"class": "wikitable"})
    for table in tables:
        attrs = table.attrs
        if (len(attrs) == 1) and ('class' in attrs):
            tbody = table.find_all('tbody', recursive=False)
            trs = tbody[0].find_all('tr')

            for tr in trs:
                ti = tr.find('i')
                if ti:
                    ta = ti.find('a')
                    if ta:
                        movie_link = ta['href']
                        if movie_link.startswith('/wiki/'):
                            movie_name = ta.get_text()
                            if movie_name not in ignore_list:
                                key = str(year) + '_' + "_".join(movie_name.lower().split())
                                movie_db[key] = {'name': movie_name, 'year': year, 'url': movie_link}

with open('../../data/movie_db.json', 'w') as fp:
    json.dump(movie_db, fp, indent=4)


with open('../../data/movie_db.json', 'r') as fp:
    movie_db = json.load(fp)

cast_db, movie_cast_db = {}, {}
base_url = 'https://en.wikipedia.org'
for movie_key in movie_db:
    movie_name = movie_db[movie_key]['name']
    movie_url = base_url + movie_db[movie_key]['url']
    movie_cast_db[movie_key] = {'name': movie_name, 'cast': []}
    print(movie_key)

    response = requests.get(url=movie_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find("div", {"class": "mw-parser-output"})
    div = div.find("div", {"class": "div-col"})
    if div:
        lis = div.find_all('li')
        for li in lis:
            tas = li.find_all('a')
            if tas and (tas[0].has_attr('title')):
                attrs = tas[0].attrs
                if ('href' in attrs) and ('title' in attrs):
                    cast_name = tas[0].get_text()
                    cast_link = tas[0]['href']
                    if cast_link.startswith('/wiki/'):
                        cast_key = "_".join(cast_name.lower().replace('.', "").split())
                        movie_cast_db[movie_key]['cast'].append(cast_key)
                        if cast_key not in cast_db:
                            cast_db[cast_key] = {'name': cast_name, 'url': cast_link}
    else:
        div = soup.find("div", {"class": "mw-parser-output"})
        uls = div.find_all('ul', recursive=False)
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                tas = li.find_all('a')
                if tas and (tas[0].has_attr('title')):
                    attrs = tas[0].attrs
                    if ('href' in attrs) and ('title' in attrs):
                        cast_name = tas[0].get_text()
                        cast_link = tas[0]['href']
                        if cast_link.startswith('/wiki/'):
                            cast_key = "_".join(cast_name.lower().replace('.', "").split())
                            movie_cast_db[movie_key]['cast'].append(cast_key)
                            if cast_key not in cast_db:
                                cast_db[cast_key] = {'name': cast_name, 'url': cast_link}


with open('../../data/cast_db.json', 'w') as fp:
    json.dump(cast_db, fp, indent=4)

with open('../../data/movie_cast_db.json', 'w') as fp:
    json.dump(movie_cast_db, fp, indent=4)


with open('../../data/cast_db.json', 'r') as fp:
    cast_db = json.load(fp)

cast_image_urls = {}
base_url = 'https://en.wikipedia.org'
for cast in cast_db:
    print(cast)
    url = cast_db[cast]['url']
    if url.startswith("/wiki/"):
        cast_url = base_url + url
    else:
        continue

    response = requests.get(url=cast_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find("div", {"class": "mw-parser-output"})
    table = div.find("table", {"class": "infobox"})
    if table:
        td = table.find("td", {"class": "infobox-image"})
        if td:
            image = td.find('img', {'src':re.compile('.jpg')})
            if image:
                image_url = 'http:'+ image['src']
                print(image_url)
                cast_image_urls[cast] = image_url
                # img = Image.open(requests.get(image_url, stream=True).raw)
                # img.save('../../data/images/' + cast + '.jpg')
                time.sleep(2)
                # img.close()

with open('../../data/cast_image_urls.json', 'w') as fp:
    json.dump(cast_image_urls, fp, indent=4)


with open('../../data/cast_image_urls.json', 'r') as fp:
    cast_image_urls = json.load(fp)

for cast in cast_image_urls:
    image_url = cast_image_urls[cast]
    print(cast, image_url)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open('../../data/images/' + cast + '.jpg','wb') as fp:
            shutil.copyfileobj(response.raw, fp)

