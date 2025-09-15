import praw
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")


# keywords to improve search results
KEYWORDS = ["review", "opinion", "experience", "impression"]


def build_query(topic):
    extra = " OR ".join(KEYWORDS)
    return f'"{topic}" ({extra})'


# connection to reddit
def reddit_connection():

    reddit = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
    )

    return reddit


def get_comments(subreddit_name, topic, post_limit, comment_limit):
    reddit = reddit_connection()
    subreddit = reddit.subreddit(subreddit_name)
    search_query = build_query(topic)
    comments = []

    for submission in subreddit.search(search_query, limit=post_limit):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list()[:comment_limit]:
            comments.append(comment.body)

    return comments
