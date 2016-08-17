#Collect a list of Yelp links to all restaurants in Toronto
import os, urllib
from bs4 import BeautifulSoup as soup
import pandas as pd
from urllib import request
import settings
import colourQuantizer

def soupTheLink(weblink):
    html = request.urlopen(weblink).read().decode('utf8')
    return soup(html, 'lxml')    
    
    
def collectLinks():
    links = []
    for page in range(0, 10, 10):
        print('starting: ' + str(page))
        mainUrl = 'https://www.yelp.ca/search?find_loc=Toronto,+ON,+Canada&start=' + str(page) + '&cflt=restaurants'
        print(mainUrl)
        
        souped = soupTheLink(mainUrl)

        count = 0

        body = souped.find(class_='search-results-content')

        for restaurant in body.find_all('li'):

            for name in restaurant.find_all(class_='biz-name js-analytics-click'):
                href = name['href']

                count += 1

                try:
                    fullLink = href[:4]  + '_photos' + href[4:] + '?tab=interior'
                    fullLink = 'https://www.yelp.ca' + fullLink
                    if count != 1:
                        links.append(fullLink)
                        settings.DATABASE['restaurant_name'].append(href[5:])

                except TypeError:
                    pass
        print(str(page) + ': is done')
        mainUrl = None
        main_html = None
        soups = None
        body = None
    print(links)
    return links
    
    
def collectPhotos(links):
    os.makedirs(settings.PHOTOS_DIR)
    os.chdir(settings.PHOTOS_DIR)
    
    for link in links:
        photos = []
        
        photoPath = '.' + link[30:-13] #trims restaurant name from url
        os.makedirs(photoPath)
        os.chdir('.' + link[30:-13])

        souped = soupTheLink(link)

        content = souped.find(class_='container')
        count = 0
        for photo in content.find_all('li'):
            for jpg in photo.find_all(class_='photo-box-img'):
                src = jpg['src']
                src = 'http:' + src
                count += 1

                filename = '.' + link[30:-13] + str(count) + '.jpg'
                photoName = link[31:-13] + str(count) + '.jpg'
                try:
                    file = urllib.request.urlretrieve(src, filename)
                    photos.append(photoName)

                except TypeError:
                    pass

        settings.DATABASE['photos'].append(photos)
        os.chdir('..')

def main():
    print("calling collectLinks")
    links = collectLinks()
    print("calling collectPhotos")
    collectPhotos(links)
    print("calling colourQuantizer.py")
    colourQuantizer.transformPhotos(settings.PHOTOS_DIR, 7)
    print("printing dataframe")
    df = pd.DataFrame(settings.DATABASE, columns = ['photos', 'restaurant_name', 'colours'])
    print(df.head())
    df.to_csv(settings.TABLE_NAME)

if __name__ == "__main__":
    main()