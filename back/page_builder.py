# -*- coding: utf-8 -*-

import csv
import os
import sys

from jinja2 import Environment, PackageLoader, select_autoescape


FRONT_DIR = '../front'
TEMPLATES_DIR = '{}/templates'.format(FRONT_DIR)
PUBLIC_DIR = '{}/public'.format(FRONT_DIR)


FILENAMES = [
    'index.html',
    'styles/general.css',
    'styles/table.css',
    'styles/interaction.css',
    'js/table.js'
]


def treat_row(row):
    treated_row = dict()

    for (key, value) in row.items():
        treated_value = value.strip()
        if (key != 'Estado') and (not treated_value.isdigit()):
            treated_value = '-'

        treated_row[key] = treated_value

    return treated_row


today = sys.argv[1]

reader = csv.DictReader(open('{}.csv'.format(today)))

RENDER_KWARGS_BY_FILENAME = {
    'index.html': {
        'header': [
            'Estado', 'Total de Casos', 'Óbitos', 'Curados', 'Suspeitos', 'Testes',
            'Novos Casos','Novos Óbitos'
        ],
        'rows': [treat_row(row) for row in reader],
        'version': open('{}/version'.format(FRONT_DIR)).read()
    }
}


env = Environment(
    loader=PackageLoader('page_builder', TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'css'])
)
env.globals.update(
    isinstance=isinstance,
    int=int
)


def build_public(filename, render_kwargs):
    template = env.get_template(filename)

    with open('{}/{}'.format(PUBLIC_DIR, filename), 'w') as f:
        rendered_html = template.render(**render_kwargs)
        f.write(rendered_html)


if __name__ == '__main__':
    for filename in FILENAMES:
        splitted = filename.rsplit('/', 1)
        parent_dirpath = PUBLIC_DIR
        if len(splitted) > 1:
            parent_dirpath = '{}/{}'.format(PUBLIC_DIR, splitted[0])
        if not os.path.exists(parent_dirpath):
            os.makedirs(parent_dirpath)

        render_kwargs = RENDER_KWARGS_BY_FILENAME.get(filename, dict())
        build_public(filename, render_kwargs)
