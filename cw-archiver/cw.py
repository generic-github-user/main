import time
import requests
import pprint
from box import Box, BoxList
from pathlib import Path
import json
import itertools

from config import cookies, headers, path, group

# db = BoxList(json.loads(Path(path).read_text()))
with open(path, "r") as db_file:
    try:
        db = Box(json.load(db_file))
    except json.decoder.JSONDecodeError as ex:
        print(ex)
        quit()
        db = Box(posts=[])

posts = db.posts
n = 20
for i in range(50):
    if posts: t = posts[-1].createdAt
    elif "last_batch" in db: t = db.last_batch
    else: t = "2022-12-30T00:00:00.000000Z"
    print(f"Fetching batch: {t}")

    response = requests.get(
        f'https://api.campuswire.com/v1/group/{group}/posts?number={n}&before={t}',
        cookies=cookies,
        headers=headers,
    )
    # breakpoint()
    data = BoxList(response.json())
    db.posts.extend(data)
    db.last_batch = t
    if len(data) == 0:
        break

    # pprint.pprint(data[0].to_dict())
    time.sleep(0.5)

checkpoint = time.time()
for attr in ["uniqueviews", "comments"]:
    for post in itertools.islice(filter(lambda x: attr not in x, db.posts), 200):
        try:
            print(f"Fetching /{attr} attribute for post: {post.title}")
            endpoint = f'https://api.campuswire.com/v1/group/{group}/posts/{post.id}/{attr}'
            response = requests.get(endpoint, cookies=cookies, headers=headers)
            data = BoxList(response.json())

            post[attr] = data
            time.sleep(0.5)
        except requests.exceptions.ConnectionError as ex:
            print(ex)

        if time.time() - checkpoint > 30:
            print("Saving checkpoint")
            db.to_json(filename=path)
            checkpoint = time.time()

db.to_json(filename=path)
