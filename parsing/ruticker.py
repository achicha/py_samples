from grab import Grab
import pyexcel
url = 'http://ruticker.com/ReportTopOrders?ticker=siz4&bigPeriod=1'
g = Grab()
g.setup(post={
    'username': "login",
    'password': "pass"
})
g.go(url)
a = []
b = []
for i in g.doc.select("//tr/td"):
    a.append(i.text())


with open('big_trades.xls', 'wt') as f:
    for elem in a:
        b.append(' '.join(str(el) for el in a[:5]))
        f.write(''.join(','.join(str(el) for el in a[:5])))
        f.write(u'\n')
        del a[:5]

