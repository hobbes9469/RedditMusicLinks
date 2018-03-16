import praw
import config
import musicsubs
from random import shuffle, randint
import webbrowser
from datetime import date

# GLOBALS containing parameters for number of submissions
# and from which time parameter the submissions are from
NUM_OF_TOP = 5
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
def get_links(reddit, sublist, saved_links_file, recycle_file):
    recycled = []
    with open(recycle_file, 'r', encoding="utf-8") as rFile:
        recycled_lines = rFile.readlines()
        for rl in recycled_lines:
            rl = rl.split("\t")
            recycled.append(rl[1])

    saved = []
    saved_links = []
    with open(saved_links_file, 'r', encoding="utf-8") as inFile:
        lines = inFile.readlines()
        for line in lines:
            row = line.split('\t')
            row[1] = row[1].rstrip()
            saved.append(row)
            saved_links.append(row[1])

    result = []     # result is a 2 dimensional array containing arrays with title and url

    for s in saved:
        result.append(s)

    for sub in sublist:
        sr = reddit.subreddit(sub)
        toplist = sr.top(time_filter=TIME_FILTER_PARAM, limit=NUM_OF_TOP)
        for submission in toplist:
            not_reddit = 'https://www.reddit.com' not in submission.url
            not_saved = submission.url not in saved_links
            not_in_recy = submission.url not in recycled
            if not_reddit and not_saved and not_in_recy:
                result.append([submission.title,submission.url.rstrip()])
    return result


# Write links to the saved links file
def save_links(links):
    with open(SAVED_LINKS_FILE, 'w', encoding='utf-8') as outFile:
        for link in links:
            tabSepRow = str(link[0]) + '\t' + str(link[1]) + '\n'
            outFile.write(tabSepRow)


# Takes in a file, returns one random link from the file and removes from list
def get_random_link(file):
    link_list = []  #Not linked list, lol
    with open(file, 'r', encoding="utf-8") as inFile:     #Populate link_list
        lines = inFile.readlines()
        for line in lines:
            item = line.split('\t')
            item[1] = item[1].rstrip()
            link_list.append(item)
    if link_list:
        for n in range(randint(1,10)):
            shuffle(link_list)
        random_link_pair = link_list[0]
        del link_list[0]
        return random_link_pair, link_list
    else:
        return ['', ''], []


# Takes a link pair to save and recycle file and appends the link to the file
def save_to_recycle(link_pair, file):
    if (link_pair[0]):  #If the first element is empty
        urls = []
        with open(file, 'r+', encoding="utf-8") as recycleFile:
            lines = recycleFile.readlines()
            recycleFile.write(link_pair[0] + '\t' + link_pair[1] + '\t' + str(date.today()) + '\n')
            for line in lines:
                urls.append(line)
        #print(urls)


def remove_old_recycle(file):
    with open(file, 'r', encoding="utf-8") as inFile:
        lines = inFile.readlines()
        #TODO: LEFT OFF HERE, parse dates and see if longer than certain period
        #TODO: If it was, delete it from the array and rewrite file after


if __name__ == "__main__":
    r = login()                                         # Login to reddit
    s = musicsubs.MUSIC_SUBS                            # Get subs to search

    while(True):
        input("Press something to get a link.")
        l = get_links(r, s, SAVED_LINKS_FILE, RECYCLE_FILE) # Get new links (possibly added to list of old links)
        save_links(l)

        rand_link_pair, saved_link_pairs = get_random_link(SAVED_LINKS_FILE)
        rand_url = rand_link_pair[1]
        if (rand_link_pair[1]):
            print(rand_url)
            # webbrowser.open(rand_url)
        else:
            print("Ran out of links! Check back later.")

        save_links(saved_link_pairs)
        remove_old_recycle(RECYCLE_FILE)
        save_to_recycle(rand_link_pair, RECYCLE_FILE)