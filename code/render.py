from frictionless import Resource, Package, FrictionlessException
from livemark.plugins.cards import CardsPlugin


# General


with Resource("data/packages.csv") as resource:
    CardsPlugin.delete_cards()
    for row in resource:

        # Package
        try:
            package = Package(row["content"])
        except FrictionlessException:
            continue

        # Card
        code = f"{row['user']}-{row['repo']}"
        CardsPlugin.create_card("cards/package.md", package=package, code=code)
