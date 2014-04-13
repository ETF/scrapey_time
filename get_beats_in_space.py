from requests import get
from bs4 import BeautifulSoup
from urlparse import urlsplit
from multiprocessing import Pool as ThreadPool
from os import rename
from id3reader import Reader

#Adjust episode range accordingly
episode_numbers = range(680, 683)


def get_music_file(episode):
    base_query = 'http://www.beatsinspace.net/playlists/%s' % episode
    html = get(base_query)
    soup = BeautifulSoup(html.text)
    links = [link.get('href') for link in soup.findAll('a')]
    mp3_urls = [link for link in links if link and link.endswith('.mp3')]
    for mp3 in mp3_urls:
        title = soup.title.string[:19]
        print 'MP3s from %s will be downloaded' % title
        with open(title, 'w') as f:
            f.write(get(mp3).content)
        x = Reader(title)
        rename(title, (x.getValue('title') + '.mp3'))

#Adjust ThreadPool count according to your own POWA!
pool = ThreadPool(10)
pool.map(get_music_file, episode_numbers)
pool.close()
pool.join()
