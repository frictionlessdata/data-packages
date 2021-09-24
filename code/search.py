import os
import json
import time
from dotenv import load_dotenv
from frictionless import Resource, transform, steps
from github import Github, RateLimitExceededException


load_dotenv()
PAUSE = 1
RETRY = 10
QUERY = "resources filename:datapackage.json path:/"
github = Github(os.environ["GITHUB_TOKEN"], per_page=100)


# Source


def fetch_source():
    source = []
    result = github.search_code(QUERY)
    time.sleep(PAUSE)
    page = 0
    while True:
        try:
            items = result.get_page(page)
        except RateLimitExceededException:
            time.sleep(RETRY)
            continue
        time.sleep(PAUSE)
        page += 1
        if not items:
            break
        for item in items:
            repo = item.repository
            file = {}
            file["user"] = repo.owner.login
            file["repo"] = repo.name
            file["branch"] = repo.default_branch
            file["path"] = item.path
            file["stars"] = repo.stargazers_count
            file["download_url"] = item.download_url
            try:
                file["content"] = json.dumps(json.loads(item.decoded_content))
            except json.JSONDecodeError:
                continue
            source.append(file)
        print(f"Found items: {len(source)}")
    return source


# General


transform(
    Resource(fetch_source()),
    steps=[
        steps.row_sort(field_names=["stars"], reverse=True),
        steps.table_write(path="data/packages.csv"),
    ],
)
