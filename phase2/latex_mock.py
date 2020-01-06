import json
import pymongo
import uuid
import datetime
from question import Question
from QBank import QBank

connection = pymongo.MongoClient("mongodb://localhost")
db = connection["latexdb"]
postings = db["T_QUESTIONS"]

mock_1 = """{
    "parent_id" : "None",
    "topics" : ["Algo","Complexity","cpp"],
    "ask_date": "None",
    "body" :"Which option is the complexity of merge sort algorithm that defined above?",
    "choices": [
        {"body":"O(n)", "iscorrect": "false", "pos": "None" },
        {"body":"O(n^2)", "iscorrect": "false", "pos": "None" },
        {"body":"O(nlog(n))", "iscorrect": "true", "pos": "None" },
        {"body":"O(log(n))", "iscorrect": "false", "pos": "None" },
        {"body":"O(1)", "iscorrect": "false", "pos": "None" }
    ],
    "embeds": [
        {"embed_url": "1"},
        {"embed_url": "2"}
    ]
}"""

mock_2 = """{
    "parent_id" : "None",
    "topics" : ["data","Algo"],
    "ask_date": "None",
    "body" : "ASDFA SADAS DAGALSKD AD?",
    "choices": [
        {"body":"asd", "iscorrect": "false", "pos": "None" },
        {"body":"aksdj", "iscorrect": "true", "pos": "None" },
        {"body":"jnskadk", "iscorrect": "false", "pos": "None" },
        {"body":"uuiq", "iscorrect": "false", "pos": "None" },
        {"body":"iqwuje", "iscorrect": "false", "pos": "None" }
    ],
    "embeds": [
        {"embed_url": "3"}
    ]
}"""

mock_3 = """{
    "parent_id" : "None",
    "topics" : ["File","python"],
    "ask_date": "None",
    "body" :"which one?",
    "choices": [
        {"body":"xd", "iscorrect": "false", "pos": "None" },
        {"body":"sdss", "iscorrect": "false", "pos": "None" },
        {"body":"xs", "iscorrect": "false", "pos": "None" },
        {"body":"qwe", "iscorrect": "true", "pos": "None" },
        {"body":"rew", "iscorrect": "false", "pos": "None" }
    ],
    "embeds": [
        {"embed_url": "4"}
    ]
}"""

mock_4 = """{
    "parent_id" : "None",
    "topics" : ["os","linux","cpp"],
    "ask_date": "None",
    "body" :"who?",
    "choices": [
        {"body":"ytr", "iscorrect": "false", "pos": "None" },
        {"body":"ref", "iscorrect": "false", "pos": "None" },
        {"body":"dndf", "iscorrect": "false", "pos": "None" },
        {"body":"bvc", "iscorrect": "false", "pos": "None" },
        {"body":"321", "iscorrect": "true", "pos": "None" }
    ],
    "embeds": [
        {"embed_url": "5"},
        {"embed_url": "6"}
    ]
}"""

mock = []
mock.append(mock_1)
mock.append(mock_2)
mock.append(mock_3)
mock.append(mock_4)

for i in range(4):
    data = json.loads(mock[i])

    body = data["body"]
    choices = data["choices"]
    topics = data["topics"]
    ask_date = None
    parent = None
    embeds = data["embeds"]

    newquestion = Question(str(uuid.uuid4()))
    newquestion.constructor(body, choices, topics, parent, embeds)

    newquestion.save()
