# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Daniel Schmidt <danischm@cisco.com>

import json
import os
import requests

# Expects the following environment variables:
# - WEBEX_TOKEN
# - WEBEX_ROOM_ID
# - Job_STATUS
# - GITHUB_REPOSITORY
# - GITHUB_RUN_NUMBER
# - GITHUB_RUN_ID
# - GITHUB_COMMIT_MESSAGE
# - GITHUB_COMMIT_URL
# - GITHUB_PULL_MESSAGE
# - GITHUB_PULL_URL
# - GITHUB_AUTHER
# - GITHUB_BRANCH
# - GITHUB_EVENT

WEBEX_TOKEN = os.getenv("BEAR_TOKEN")
WEBEX_ROOM_ID = os.getenv("ROOMID")
Job_STATUS = str(os.getenv("Job_STATUS") or "").lower()
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_RUN_NUMBER = os.getenv("GITHUB_RUN_NUMBER")
GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")
GITHUB_COMMIT_MESSAGE = os.getenv("GITHUB_COMMIT_MESSAGE")
GITHUB_COMMIT_URL = str(os.getenv("GITHUB_COMMIT_URL") or "")
GITHUB_PULL_MESSAGE = os.getenv("GITHUB_PULL_MESSAGE")
GITHUB_PULL_URL = str(os.getenv("GITHUB_PULL_URL") or "")
GITHUB_AUTHER = os.getenv("GITHUB_AUTHER")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")
GITHUB_EVENT = os.getenv("GITHUB_EVENT")
WORKFLOW_NAME = os.getenv("WORKFLOW_NAME")
REQ_TIMEOUT = os.getenv("REQ_TIMEOUT")


VALIDATION_OUTPUT = """\n**Validation Errors**
```
"""

TEST_OUTPUT = """\n[**Testing**](https://github.com/guilinyan/actions/blob/gh-pages/log.html)
```
"""

def create_webex_card():
    IMAGE_URL = None
    TEXT_MESSAGE = None
    COLOR = None
    ACTION_STYLE = None
    if Job_STATUS == "success":
        IMAGE_URL = "https://s2.loli.net/2022/04/15/fukZBA9RpPFKrbM.jpg"
        TEXT_MESSAGE = f"Github Pipeline {WORKFLOW_NAME} succeeded!"
        COLOR = "Good"
        ACTION_STYLE = "positive"
    else:
        IMAGE_URL = "https://s2.loli.net/2022/04/15/xnrdqf85USK3owA.jpg"
        TEXT_MESSAGE = f"Github Pipeline {WORKFLOW_NAME} failed!"
        COLOR = "Warning"
        ACTION_STYLE = "destructive"

    MESSAGE = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content":{
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "Image",
                                    "style": "Person",
                                    "url": IMAGE_URL,
                                    "size": "Medium",
                                    "height": "50px"
                                }
                            ],
                            "width": "auto"
                        },
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "Cisco Software Team",
                                    "weight": "Lighter",
                                    "color": "Accent"
                                },
                                {
                                    "type": "TextBlock",
                                    "weight": "Bolder",
                                    "text": TEXT_MESSAGE,
                                    "horizontalAlignment": "Left",
                                    "wrap": True,
                                    "color": COLOR,
                                    "size": "Large",
                                    "spacing": "None"
                                }
                            ],
                            "width": "stretch"
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "width": 35,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "WorkFlow ID:",
                                    "color": "Light",
                                    "spacing": "Small",
                                    "weight": "Lighter"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Commit:",
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Author:",
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Branch:",
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Event:",
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": 100,
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": GITHUB_REPOSITORY + " #" + GITHUB_RUN_NUMBER,
                                    "color": "Light",
                                    "weight": "Lighter",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": GITHUB_COMMIT_MESSAGE + GITHUB_PULL_MESSAGE,
                                    "color": "Light",
                                    "weight": "Lighter",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": GITHUB_AUTHER,
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": GITHUB_BRANCH,
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": GITHUB_EVENT,
                                    "weight": "Lighter",
                                    "color": "Light",
                                    "spacing": "Small"
                                }
                            ]
                        }
                    ],
                    "spacing": "Padding",
                    "horizontalAlignment": "Center"
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "Open Github Pipline",
                            "style": ACTION_STYLE,
                            "url": "https://github.com/" + GITHUB_REPOSITORY + "/actions/runs/" + GITHUB_RUN_ID
                        },
                        {
                            "type": "Action.OpenUrl",
                            "title": "Open Commit Link",
                            "style": ACTION_STYLE,
                            "url": GITHUB_COMMIT_URL + GITHUB_PULL_URL
                        }
                    ],
                    "spacing": "Small",
                    "horizontalAlignment": "Center"
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.3"
        }
    }
    return MESSAGE, TEXT_MESSAGE

if __name__ == "__main__":
        
    data, TEXT_MESSAGE = create_webex_card()
    post_data = {
        "roomId": WEBEX_ROOM_ID,
        "text": TEXT_MESSAGE,
        "attachments": data,
        "toPersonEmail": None,
        "markdown": None,
        "parentId": None,
    }
    Msg_url = "https://api.ciscospark.com/v1/messages"
    Msg_headers = {
        "Authorization": "Bearer %s" % WEBEX_TOKEN,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(Msg_url, headers=Msg_headers, data=json.dumps(post_data), timeout=int(REQ_TIMEOUT))
        resp.raise_for_status()
    except requests.HTTPError as except_error:
        # possibly check response for a message
        raise except_error
    except requests.Timeout as except_timeout:
        # request took too long
        raise except_timeout