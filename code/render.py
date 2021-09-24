from frictionless import Resource, Package
from livemark.plugins.cards import CardsPlugin


# General


with Resource("data/packages.csv") as resource:
    CardsPlugin.delete_cards()
    for row in resource:
        code = f"{row['user']}-{row['repo']}"
        package = Package(row["content"])
        CardsPlugin.create_card("cards/package.md", package=package, code=code)
        break
