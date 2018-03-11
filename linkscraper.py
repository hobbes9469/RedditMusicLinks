import praw
import config
import musicsubs
from random import shuffle, randint
import webbrowser
from datetime import date

# GLOBALS containing parameters for number of submissions
# and from which time parameter the submissions are from
NUM_OF_TOP = 25
TIME_FILTER_PARAM = 'week'

# GLOBAL containing list of sites to accept for saved links
SITES = [
    'youtube.com', 'youtu.be', 'soundcloud.com', 'bandcamp.com',
]

SAVED_LINKS_FILE = 'saved_links.txt'
RECYCLE_FILE = 'recycle.txt'


# Logs in with credentials and returns the reddit instance
def login():
    reddit = praw.Reddit(user_agent = "redandbluetheme's music link script",
                         username = config.username, password = config.password,
                         client_id = config.client_id, client_secret = config.client_secret)
    return reddit


# Takes reddit instance, and list of subreddits
# Returns 2D array of (title, link) pairs of top music lists
def get_links(reddit, sublist, file):
    saved = []
    with open(file, 'r') as inFile:
        lines = inFile.readlines()
        for line in lines:
            link_pair = line.split('\t')
            saved.append(link_pair[1])

    result = []     # result is a 2 dimensional array containing arrays with title and url
    for sub in sublist:
        sr = reddit.subreddit(sub)
        toplist = sr.top(time_filter=TIME_FILTER_PARAM, limit=NUM_OF_TOP)
        for submission in toplist:
            if ('https://www.reddit.com' not in submission.url) and (submission.url not in saved):
                result.append([submission.title,submission.url.rstrip()])
    return result


# Write links to file, returns
def save_links(links):
    with open(SAVED_LINKS_FILE, 'w', encoding='utf-8') as outFile:
        for link in links:
            tabSepRow = str(link[0].encode("utf-8")) + '\t' + str(link[1]) + '\n'
            outFile.write(tabSepRow)


# Takes in a file, returns one random link from the file and removes from list
def get_random_link(file):
    link_list = []
    with open(file, 'r') as inFile:     #Populate link_list
        lines = inFile.readlines()
        for line in lines:
            item = line.split('\t')
            item[1] = item[1].rstrip()
            link_list.append(item)
    for n in range(randint(1,10)):
        shuffle(link_list)
    random_link_pair = link_list[0]
    del link_list[0]
    return random_link_pair, link_list


def save_to_recycle(url, file):
    urls = []
    with open(file,'r+') as recycleFile:
        lines = recycleFile.readlines()
        recycleFile.write(url + '\t' + str(date.today()) + '\n')
        for line in lines:
            urls.append(line)
    print(urls)


def remove_old_recycle(file):
    with open(file, 'r') as inFile:
        lines = inFile.readlines()
        #TODO: LEFT OFF HERE, parse dates and see if longer than certain period
        #TODO: If it was, delete it from the array and rewrite file after
        

if __name__ == "__main__":
    r = login()
    s = musicsubs.MUSIC_SUBS
    l = get_links(r, s, SAVED_LINKS_FILE)
    save_links(l)

    rand_link_pair, saved_link_pairs = get_random_link(SAVED_LINKS_FILE)
    rand_url = rand_link_pair[1]
    print(rand_url)
    #webbrowser.open(rand_url)
    save_links(saved_link_pairs)
    remove_old_recycle(RECYCLE_FILE)
    save_to_recycle(rand_url, RECYCLE_FILE)