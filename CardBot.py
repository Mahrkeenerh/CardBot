import praw, datetime, sys, json
from time import sleep

with open("config.txt") as config_file:

    config_json = json.load(config_file)

    userAgent = config_json['userAgent']
    cID = config_json['cID']
    cSC = config_json['cSC']
    userN = config_json['userN']
    userP = config_json['userP']

    reddit = praw.Reddit(user_agent=userAgent, 
        client_id=cID, 
        client_secret=cSC, 
        username=userN, 
        password=userP)

    subreddit = reddit.subreddit(config_json['subreddit'])

start_time = datetime.datetime.now()

while True:
    try:
        with open("database.json") as json_file:
            data_dict = json.load(json_file)

        for comment in subreddit.stream.comments():
            comment_time = datetime.datetime.fromtimestamp(comment.created_utc)

            # only check new comments
            if comment_time > start_time:
                lowercase_body = comment.body.lower().replace("\\", "")

                for keyword in [x.split("]]")[0] for x in lowercase_body.split("[[") if "]]" in x]:
                    if keyword in data_dict:
                        out_string = "| | |\n|-|-|\n"
                        for i in data_dict[keyword]:
                            out_string += "|__" + i[0] + "__|" + i[1] + "|\n"
                        
                        comment.reply(out_string)

    # An error - sleep and hope it works now
    except:
        print("\n", datetime.datetime.now())
        print("En error occured with inbox")
        print(sys.exc_info())
        sleep(60)
