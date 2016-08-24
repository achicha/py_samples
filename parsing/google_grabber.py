# -*- coding: utf-8 -*-
from grab import Grab

g = Grab()

g.go('google.ru')
#search 'grab python' in search panel (name='q')
g.doc.set_input('q', 'grab python')
#push search button
g.doc.submit(submit_name='btnG')
#use select with xpath expressions
for y in g.doc.select("//h3[@class = 'r']//a"):
    print(y.text(), y.attr('href'))
    #print (y.html())