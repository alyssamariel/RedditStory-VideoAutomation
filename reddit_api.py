import praw
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(
    client_id = config["reddit"]["client_id"],
    client_secret = config["reddit"]["client_secret"],
    username = config["reddit"]["username"], 
    password = config["reddit"]["password"], 
    user_agent = config["reddit"]["user_agent"]
)

# get reddit post title for title card and voiceover
def get_reddit_post_title(url):
    submission = reddit.submission(url=url)
    return submission.title


# get reddit comments for the voiceover
def get_reddit_post_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=50)
    
    all_comments = submission.comments.list()
    selected_comments = []
    
    i = 0
    while i < len(all_comments):
        batch = all_comments[i:i+3]
        for comment in batch:
            print("\nComment:")
            print(comment.body)
            choice = input(" Add this comment to your list? (y/n): ").strip().lower()
            if choice == 'y':
                selected_comments.append(comment.body)
        i += 3

        if i < len(all_comments):
            cont = input("\n Show next 3 comments? (y/n): ").strip().lower()
            if cont != 'y':
                break
    
    print("\n Selected Comments:")
    for idx, c in enumerate(selected_comments, 1):
        print(f"{idx}. {c}")

    return selected_comments