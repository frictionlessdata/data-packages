from github import Github
from frictionless import Resource, transform, steps


IGNORE_PATH = ["node_modules", "test", "fixture", "output", "example"]
github = Github("token", per_page=100)
cache = {}


# Steps


def row_filter_function(row):
    if not row["path"].endswith("datapackage.json"):
        return False
    for pattern in IGNORE_PATH:
        if pattern in row["path"]:
            return False
    return True


def field_add_function(row):
    name = "/".join([row["user"], row["repo"]])
    stars = cache.get(name)
    if not stars:
        repo = github.get_repo(name)
        stars = cache[name] = repo.stargazers_count
    return stars


# General


transform(
    Resource("data/search.csv"),
    steps=[
        steps.row_filter(function=row_filter_function),
        steps.field_add(name="stars", function=field_add_function),
        steps.row_sort(field_names=["stars"], reverse=True),
        steps.table_write(path="data/filter.csv"),
    ],
)
