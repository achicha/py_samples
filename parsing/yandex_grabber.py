# -*- coding: utf-8 -*-
from grab import Grab

g = Grab()
words = 'grab, python'
lst = []
#go to url (moscow region: rstr=-213) (page: p=0) with text
url = 'http://yandex.ru/yandsearch?rstr=-213&p={0}&text={1}'
#add keywords to the link
param = words.replace(" ", "").split(',')
param2 = '%2C+'.join(str(elem) for elem in param)

#write to file
with open('somefile.txt', 'wt') as f:
    for page in range(3):
        fullurl = url.format(page, param2)
        g.go(fullurl)
        #using selectors to get a full href list
        for i in g.doc.select('//a[@class="b-link serp-item__title-link serp-item__title-link"]'):
            if g.doc.select('//a[@class="b-link serp-item__title-link serp-item__title-link"]').exists():

                lst.append({'page': page+1, 'title': i.text(), 'url': i.attr('href')})
                #print(i.text())
                f.write(i.attr('href'))
                f.write('\n')
print(lst)
