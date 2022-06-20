from pprint import pprint
from frictionless import Resource, transform, steps


# General


transform(
    Resource(path="data/packages.csv"),
    steps=[
        steps.table_merge(resource=Resource(path="data/packages.raw.csv")),
        steps.table_normalize(),
        steps.row_sort(field_names=["stars"], reverse=True),
        steps.table_write(path="data/packages.csv"),
    ],
)
