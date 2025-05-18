import praw

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    username='',
    password='',
    user_agent=''
)


def get_reddit_post_title(url):
    submission = reddit.submission(url=url)
    return submission.title
