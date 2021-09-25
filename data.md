# Data Collection

## Search packages

First of all, we need to find all the data packages on Github. We're going to look at all the repos having `datapackage.json` in the root directory. Github Search API has quite strict querying limits so we have to use different techniques to avoid rate limit errors. As a high-level data collections framework, we will use Frictionless Transform. It will sort the packages by repository's stargazers count and save it to the CSV file:

```bash
$ python code/search.py
```

```python file
code/search.py
```

## Render packages

After we have the `packages.csv` file filled with data packages, we need to render them as Livemark Cards. To achieve this task we will use builtin methods that comes with the Cards plugin:

```bash
$ python code/render.py
```

```python file
code/render.py
```
