import logging
import requests

# basic
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# write all logs to file
formatter = logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s','%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('my1.log', 'a')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
handler.propagate = True

# log request library with our handler
requests_log = logging.getLogger("requests")
requests_log.addHandler(handler)

# do something with request library
r = requests.get('http://httpbin.org/get?key=value')
r = requests.post('http://httpbin.org/post', data={'key':'value'})
