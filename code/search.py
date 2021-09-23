import time
from github import Github
from random import randint
from frictionless import Resource


SLEEP = 15
QUERY = "filename:datapackage.json size:%s..%s"
github = Github("token", per_page=100)


# Source


def fetch_source():
    size = 0
    source = []
    while True:

        # Get pages
        slice = (1 + size // 1000) * 100
        result = github.search_code(query=QUERY % (size, size + slice - 1))
        time.sleep(SLEEP + randint(1, SLEEP))
        size += slice
        if not result.totalCount:
            break

        # Iterage pages
        page = 0
        while True:
            items = result.get_page(page)
            time.sleep(SLEEP + randint(1, SLEEP))
            page += 1
            if not items:
                break
            for item in items:
                file = {}
                file["user"] = item.repository.owner.login
                file["repo"] = item.repository.name
                file["path"] = item.path
                file["url"] = item.url
                source.append(file)
            print(f"Found items: {len(source)}")
        break

    return source


# General


resource = Resource(fetch_source())
resource.write("data/search.csv")
