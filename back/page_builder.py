# -*- coding: utf-8 -*-

import csv
import os

from jinja2 import Environment, PackageLoader, select_autoescape


FRONT_DIRPATH = os.environ.get('FRONT_DIRPATH')
TEMPLATES_DIRPATH = os.environ.get('TEMPLATES_DIRPATH')
PUBLIC_DIRPATH = os.environ.get('PUBLIC_DIRPATH')


DEFAULT_FILENAMES = [
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


file = open('data.csv')
reader = csv.DictReader(file)

RENDER_KWARGS_BY_FILENAME = {
    'index.html': {
        'header': [
            'Estado', 'Total de Casos', 'Óbitos', 'Curados', 'Suspeitos', 'Testes',
            'Novos Casos','Novos Óbitos'
        ],
        'rows': [treat_row(row) for row in reader],
        'version': open('{}/version'.format(FRONT_DIRPATH)).read()
    }
}


env = Environment(
    loader=PackageLoader('page_builder', TEMPLATES_DIRPATH),
    autoescape=select_autoescape(['html', 'css'])
)
env.globals.update(
    isinstance=isinstance,
    int=int
)


def build_public(filename, render_kwargs):
    template = env.get_template(filename)

    with open('{}/{}'.format(PUBLIC_DIRPATH, filename), 'w') as f:
        rendered_html = template.render(**render_kwargs)
        f.write(rendered_html)


def build(filenames):
    for filename in filenames:
        splitted = filename.rsplit('/', 1)
        parent_dirpath = PUBLIC_DIRPATH
        if len(splitted) > 1:
            parent_dirpath = '{}/{}'.format(PUBLIC_DIRPATH, splitted[0])
        if not os.path.exists(parent_dirpath):
            os.makedirs(parent_dirpath)

        render_kwargs = RENDER_KWARGS_BY_FILENAME.get(filename, dict())
        build_public(filename, render_kwargs)


if __name__ == '__main__':
    build(DEFAULT_FILENAMES)
