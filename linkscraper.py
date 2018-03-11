import praw
import config
import musicsubs

# Globals containing parameters for number of submissions
# and from which time parameter the submissions are from
NUM_OF_TOP = 10
TIME_FILTER_PARAM = 'week'


# Logs in with credentials and returns the reddit instance
def login():
    reddit = praw.Reddit(user_agent = "redandbluetheme's music link script",
                         username = config.username, password = config.password,
                         client_id = config.client_id, client_secret = config.client_secret)
    return reddit


# TODO: only get links if they are from soundcloud or youtube (maybe spotify)
# Takes reddit instance, and list of subreddits
# Returns 2D array of (title, link) pairs of top music lists
def get_links(reddit, sublist):
    result = []     # result is a 2 dimensional array containing arrays with title and url
    for sub in sublist:
        sr = reddit.subreddit(sub)
        toplist = sr.top(time_filter=TIME_FILTER_PARAM, limit=NUM_OF_TOP)
        for submission in toplist:
            result.append([submission.title,submission.url])
    return result


# Write links to file
def save_links(links):
    with open('saved_links.txt', 'w', encoding='utf-8') as outFile:
        for link in links:
            tabSepRow = str(link[0].encode("utf-8")) + '\t' + str(link[1]) + '\n'
            outFile.write(tabSepRow)


if __name__ == "__main__":
    r = login()
    s = musicsubs.MUSIC_SUBS
    l = get_links(r,s)
    save_links(l)
