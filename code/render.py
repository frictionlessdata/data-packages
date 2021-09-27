from frictionless import Resource, Package
from livemark.plugins.cards import CardsPlugin


# General


with Resource("data/packages.csv") as resource:
    CardsPlugin.delete_cards()
    for row in resource:
        code = row["code"]
        package = Package(row["content"])
        CardsPlugin.create_card("cards/package.md", code=code, package=package)
