from frictionless import Resource
from livemark.plugins.cards import CardsPlugin


# General


with Resource("data/filter.csv") as resource:
    CardsPlugin.delete_cards()
    for row in resource:
        code = f"row['user']/row['repo']/row['path']"
        CardsPlugin.create_card("cards/package.md", code=code, name="Test")
