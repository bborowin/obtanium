import prowlpy, requests, json
from models.local import SearchNotification as sn


prowl_api_key = 'de026b5718d99fa0d26042a814a1d79655212cb2'

class Notifier(object):
    def __init__(self):
        self.p = prowlpy.Prowl(prowl_api_key)

    def send(self):
        nots = sn.query.filter(sn.status=='new')
        for n in nots:
            n.status = 'sent'
            title = '${0} {1}.5'.format(n.apt.price,n.apt.rooms)
            address = n.apt.location.address[:40]
            map_link = "https://maps.google.ca/maps?q={0},{1}".format(n.apt.location.latitude, n.apt.location.longitude)
            url = self.shortenUrl(map_link)
            self.p.add(address, title, url, 1, None, n.apt.url.value)
            print n

    def shortenUrl(self, url):
        data = '{"longUrl": "'+url+'"}'
        r = requests.post('https://www.googleapis.com/urlshortener/v1/url', data=data, headers = {"Content-Type": "application/json"})
        if 200 == r.status_code:
            return json.loads(r.content)['id']
        else:
            return url
