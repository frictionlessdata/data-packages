import os
import json
import time
from dotenv import load_dotenv
from github import Github, RateLimitExceededException
from frictionless import Package, Resource, transform, steps
from frictionless import FrictionlessException


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
            data = {}
            data["code"] = "-".join([repo.owner.login, repo.name])
            data["user"] = repo.owner.login
            data["repo"] = repo.name
            data["branch"] = repo.default_branch
            data["path"] = item.path
            data["stars"] = repo.stargazers_count
            data["download_url"] = item.download_url
            try:
                package = Package(json.loads(item.decoded_content))
                data["title"] = package.title
                data["description"] = package.description_text
                data["content"] = json.dumps(package.to_dict())
            except (json.JSONDecodeError, FrictionlessException):
                continue
            source.append(data)
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
