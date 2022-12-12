import time
import requests
import pprint
from box import Box, BoxList
from pathlib import Path
import json
import itertools

from config import cookies, headers, groups
groups = BoxList(groups)

def fetch_post(db, group, post, attr):
    try:
        print(f"Fetching /{attr} attribute for post: {post.title}")
        endpoint = f'https://api.campuswire.com/v1/group/{group.id}/posts/{post.id}/{attr}'
        response = requests.get(endpoint, cookies=cookies, headers=headers)
        if response.status_code != 404:
            try:
                data = BoxList(response.json())
            except requests.exceptions.JSONDecodeError as ex:
                breakpoint()
                print(ex)
                # print(response)

            post[attr] = data
        else:
            print(response)
        time.sleep(0.5)
    except requests.exceptions.ConnectionError as ex:
        print(ex)

    if time.time() - db.checkpoint > 30:
        print("Saving checkpoint")
        db.to_json(filename=group.path)
        db.checkpoint = time.time()

def update_class(group):
    print(f"Fetching {group}")
    # db = BoxList(json.loads(Path(path).read_text()))
    try:
        with open(group.path, "r") as db_file:
            try:
                db = Box(json.load(db_file))
            except json.decoder.JSONDecodeError as ex:
                print(ex)
                quit()
                db = Box(posts=[])
    except FileNotFoundError as ex:
        print(ex)
        db = Box(posts=[])

    posts = db.posts
    n = 20
    for i in range(50):
        if posts: t = posts[-1].createdAt
        elif "last_batch" in db: t = db.last_batch
        else: t = "2022-12-30T00:00:00.000000Z"
        print(f"Fetching batch: {t}")

        response = requests.get(
            f'https://api.campuswire.com/v1/group/{group.id}/posts?number={n}&before={t}',
            cookies=cookies,
            headers=headers,
        )
        data = BoxList(response.json())
        db.posts.extend(data)
        db.last_batch = t
        if len(data) == 0:
            break

        # pprint.pprint(data[0].to_dict())
        time.sleep(0.5)

    db.checkpoint = time.time()
    for attr in group.attrs:
        for post in itertools.islice(filter(lambda x: attr not in x, db.posts), 200):
            fetch_post(db, group, post, attr)

    db.to_json(filename=group.path)

for G in groups:
    update_class(G)
