import discord
import asyncio
from random import randint
from urllib.parse import quote
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET

client = discord.Client()

WORDS_FILE = 'words.txt'
URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&"
GET_PAGE_ID = "redirects&titles="
GET_IMAGES = "prop=images&pageids="
GET_IMAGE_URL = "prop=imageinfo&iiprop=url&iiurlwidth=220&titles="
BITLY_URL = "https://api-ssl.bitly.com/v3/shorten?access_token=4e9fe114c60e41a288160a27d1f0f49e9857bc87&longUrl="
CHAT_BOT_URL = "http://www.botlibre.com/rest/botlibre/form-chat?instance=165&message="

@client.event
async def on_ready():
    print('Logged in as %s, (id %s).' % (client.user.name, client.user.id))
    print('Discord version: %s' % discord.__version__)

@client.event
async def on_message(msg):
    txt = msg.content.lower()
    if txt.startswith('/kill'):
        await client.send_message(msg.channel, 'I am so sorry, I did not want to disturb you... I\'m dying now. Bye.')
        await client.logout()
    elif msg.mention_everyone and randint(1, 2):
        await client.send_message('ok!')
    elif 'Roipoubot' in [m.name for m in msg.mentions]:
        if 'time' in txt.split(' '):
            await client.send_message(msg.channel, 'https://www.youtube.com/watch?v=oA1vp8p_V3Y')
        elif any(word in txt for word in ['stupid', 'sucks', 'tg']):
            await client.send_message(msg.channel, 'http://i.imgur.com/oPe6BBn.jpg')
        else:
            await client.send_message(msg.channel, chat(txt))
    elif txt.startswith('/quote'):
        await client.send_message(msg.channel, random_pic())
    elif 'où' in txt.split(' '):
        await client.send_message(msg.channel, 'dtc')
    elif 'gros' in txt.split(' '):
        await client.send_message(msg.channel, 'cmb')
    elif 'long' in txt.split(' '):
        await client.send_message(msg.channel, 'cmb')
    elif 'dur' in txt.split(' '):
        await client.send_message(msg.channel, 'cmb')
    else:
        words = msg.content.split(' ')
        for word in words:
            if word.startswith('di') and word != 'discord':
                await client.send_message(msg.channel, word[2:])

### commands functions ###

def chat(text):
    uri = CHAT_BOT_URL + quote(text)
    print(uri)
    res = ET.fromstring(urlopen(uri).read().decode("utf-8", "ignore"))[0].text
    return res

def random_pic():
    # title, url = get_random_thumb_url() #debug
    while True: #prod
        try:
            title, url = get_random_thumb_url()
            break
        except:
            print('\nAn error occured. Trying with an other word.\n')

    return 'and here is a %s picture ' % title + url

### utils ###

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_random_word():
    nb_words = file_len(WORDS_FILE)
    rand = randint(0, nb_words)
    with open(WORDS_FILE) as f:
        for i, l in enumerate(f):
            if i == rand:
                return(l.strip())

def shortify(url):
    uri = BITLY_URL + quote(url, safe='')
    res = json.loads(urlopen(uri).read().decode("utf-8", "ignore"))
    if res['status_code'] != 200:
        raise Exception('bitly API returned a bad response code:\nuri:' + uri + '\nresponse code: ' + res['status_code'] + ': ' + status_txt)
    return res['data']['url']

def wiki_query(query, value):
    uri = URL + query + quote(str(value))
    res = json.loads(urlopen(uri).read().decode("utf-8", "ignore"))
    if 'warnings' in res:
        raise Exception('Mediawiki API returned a warning:\nuri:' + uri + '\nwarnings: ' + res['warnings'])
    return list(res['query']['pages'].values())[0]

def get_random_page_id():
    while True:
        word = get_random_word()
        res = wiki_query(GET_PAGE_ID, word)
        if 'pageid' in res and res['pageid'] != '-1':
            return word, res['title'], res['pageid']

def get_image_title(page_id):
    res = wiki_query(GET_IMAGES, page_id)
    image_title = res['images'][0]['title']
    return image_title

def get_random_thumb_url():
    while True:
        word, title, page_id = get_random_page_id()
        image_title = get_image_title(page_id)
        print('word: %s ; page title: %s ; page id:%s ; image title:%s'
            % (word, title, page_id, image_title))
        if image_title[-4:] != '.svg':
            break # pass wikipedia pictures (disanbiguation, etc.)
    thumb_url = wiki_query(GET_IMAGE_URL, image_title)['imageinfo'][0]['thumburl']
    short_url = shortify(thumb_url)
    print('short url:', short_url)
    return title, short_url

client.run('MAIL', 'PASSWORD')