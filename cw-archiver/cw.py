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
