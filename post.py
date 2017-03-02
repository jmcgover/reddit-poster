#! /usr/bin/env python3

import os
import sys

import praw
import json

from argparse import ArgumentParser
DEFAULT_AUTH=os.path.expanduser("~/.ssh/authentication.json")
DESCRIPTION="Posts to a provided subreddit."
def get_arg_parser():
    parser = ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    # Authentication
    parser.add_argument("-a","--authentication",
            nargs=1,
            metavar="authentication.json",
            default=[DEFAULT_AUTH],
            dest="authentication",
            help="authentication containing user agent, client id and secret, password, and username")
    # Subreddit
    parser.add_argument(
            metavar="subreddit",
            dest="subreddit",
            help="name of the subreddit to post to")
    # Title
    parser.add_argument(
            metavar="title",
            dest="title",
            help="title of post")
    # Post
    parser.add_argument(
            metavar="post",
            dest="post",
            help="post: text if --text, a link otherwise")
    # Text
    parser.add_argument("-t","--text",
            action="store_true",
            default=False,
            help="post as a text post")
    return parser

def post_to_json(post):
    post_json = {key:val for key,val in post.__dict__.items()}
    for key,val in post_json.items():
        if isinstance(val,praw.models.reddit.redditor.Redditor) \
                or isinstance(val,praw.models.reddit.subreddit.Subreddit) \
                or isinstance(val,praw.Reddit):
            post_json[key] = "%s" % val
    return post_json

class RedditPoster(object):
    def __init__(self, user_agent, client_id, client_secret, username, password):
        self.reddit = praw.Reddit(
                        user_agent      =user_agent,
                        client_id       =client_id,
                        client_secret   =client_secret,
                        username        =username,
                        password        =password)
        return
    def submit(self, subreddit, title, post, text_post = False):
        result = None
        subreddit = self.reddit.subreddit(subreddit)
        if text_post:
            assert False, "text posts not implemented yet"
        else:
            result = subreddit.submit(title, url = post)
        return result

def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    print("Authentication:%s" % args.authentication[0])
    print("Subreddit:%s" % args.subreddit)
    print("Title:%s" % args.title)
    print("Post:%s" % args.post)
    auth = {}
    with open(args.authentication[0]) as file:
        auth = json.load(file)
    poster = RedditPoster(
            auth["user_agent"],
            auth["client_id"],
            auth["client_secret"],
            auth["username"],
            auth["password"])
    result = poster.submit(args.subreddit, args.title, args.post, args.text)
    print(result)
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
