import discord
import asyncio
from random import randint
from urllib.parse import quote
from urllib.request import urlopen
import json

client = discord.Client()

WORDS_FILE = 'words.txt'
URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&"
GET_PAGE_ID = "redirects&titles="
GET_IMAGES = "prop=images&pageids="
GET_IMAGE_URL = "prop=imageinfo&iiprop=url&iiurlwidth=220&titles="

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('/quote'):

        while True:
            try:
                title, url = get_random_thumb_url()
                break
            except:
                print('\nA strange error occured. Trying with an other word.\n')

        text = 'and there is an image of ' + title + ' ' + url
        await client.send_message(message.channel, text)

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

def wiki_query(query, value):
    uri = URL + query + quote(str(value))
    res = urlopen(uri).read().decode("utf-8", "ignore")
    return(list(json.loads(res)["query"]['pages'].values())[0])

def get_random_page_id():
    while True:
        word = get_random_word()
        res = wiki_query(GET_PAGE_ID, word)
        if 'pageid' in res and res['pageid'] != '-1':
            return(word, res['title'], res['pageid'])

def get_image_title(page_id):
    res = wiki_query(GET_IMAGES, page_id)
    #TODO: do not get disambig
    image_title = res['images'][0]['title']
    return(image_title)

def get_random_thumb_url():
    while True:
        word, title, page_id = get_random_page_id()
        image_title = get_image_title(page_id)
        print('word: %s ; page title: %s ; page id:%s ; image title:%s'
            % (word, title, page_id, image_title))
        if image_title[-4:] != '.svg': break # pass wikipedia pictures
    thumb = wiki_query(GET_IMAGE_URL, image_title)['imageinfo'][0]['thumburl']
    print('thumbnail url:', thumb)
    return(title, thumb)

client.run('MAIL', 'PASSWORD')