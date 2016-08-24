#!/usr/bin/python
# -*- coding: utf-8 -*-
from grab import Grab
from urllib.request import urlopen
import os
import zipfile
import glob
import requests

def generate_genre_links(names):
    # print('generating links')
    new_names = []
    for name in names:
        new_names.append('http://flibusta.net/g/%s/Pop' % name)
    # print('finish generating links')
    return new_names


def download_fb2(links, dir, limit):
    for link in links:
        g = Grab()
        g.go(link)
        genre = g.doc.select('//*[@id="main"]/h1').text()
        # try:
        #     os.makedirs(genre)
        # except OSError:
        #     pass
        book_links = g.doc.select('//*[@id="main"]/form/ol/a')
        i = 0  # add limit counter

        for book_link in book_links:
            if i == limit:
                break
            link = 'http://flibusta.net%s/fb2' % book_link.attr('href')
            name = book_link.text()
            book_url = urlopen(link)
            book = book_url.read()
            try:
                book.decode('utf-8')
                print('Book %s is blocked' % name)
                continue
            except UnicodeDecodeError:
                pass

            completeName = os.path.join("{0}\\{1}\\{2}.zip".format(dir, genre, name))

            #if timout error, do it again
            while True:
                try:
                    f = open(completeName, 'wb')
                    f.write(book)
                    f.close()
                    i += 1
                    print('downloaded: ' + name)
                except requests.exceptions.RequestException as e:    # This is the correct syntax
                    print(e)
                    continue
                break

        else:
            print('Finished %s' % genre)


if __name__ == '__main__':
    genres = ['detective']
    '''
        'det_action', 'det_irony', 'det_history', 'det_classic',
         'det_crime', 'det_hard', 'det_political', 'det_police', 'det_maniac',
         'det_su', 'thriller', 'det_espionage']
    '''
    path = ""  # "C:\\Users\\andreyev\\PycharmProjects\\hh\\py_class"
    links = generate_genre_links(genres)
    download_fb2(links, path, 2)  # how many books from each genre
    print("downloaded")

    # unzip all files
    files = glob.glob('*.zip')
    for file in files:
        zipfile.ZipFile(file).extractall(os.path.dirname(file))  # extract to parent directory
    print("Unzipped")


    #rename files
    for filename in glob.glob('*.fb2'):
        #take first 2 words from name
        #new_name = os.path.basename(filename).split('_')[0]+'_'+os.path.basename(filename).split('_')[1]+'.fb2'
        try:
            #new_name = "_".join(os.path.basename(filename).split('_')[:-1])+'.fb2'
            new_name = "_".join(os.path.basename(filename).split('.')[:-2])+'.fb2'
        except FileNotFoundError:
            continue
        try:
            os.rename(
                os.path.join(os.path.dirname(filename), os.path.basename(filename)),
                os.path.join(os.path.dirname(filename), new_name)
            )
        except PermissionError:
            continue
    print("renamed")

