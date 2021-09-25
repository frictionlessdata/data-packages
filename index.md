# Data Packages

## Introduction

text here

## Catalogue

{% for row in frictionless.extract('data/packages.csv') %}
**{{ row.user }}/{{ row.repo }}**
[Link](#card={{ row.user }}-{{ row.repo }})

{% endfor %}
