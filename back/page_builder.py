# -*- coding: utf-8 -*-

import csv
import sys

from jinja2 import Environment, PackageLoader, select_autoescape


DATA_DIR = 'data'

FRONT_DIR = '../front'
TEMPLATES_DIR = '{}/templates'.format(FRONT_DIR)
PUBLIC_DIR = '{}/public'.format(FRONT_DIR)


FILENAMES = [
    'index.html', 'styles.css', 'table-styles.css'
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

reader = csv.DictReader(open('{}/{}.csv'.format(DATA_DIR, today)))

RENDER_KWARGS_BY_FILENAME = {
    'index.html': {
        'header': [
            'Estado', 'Total de Casos', 'Óbitos', 'Curados', 'Suspeitos', 'Testes',
            'Novos Casos','Novos Óbitos'
        ],
        'rows': [treat_row(row) for row in reader],
        'version': open('{}/version'.format(FRONT_DIR)).read()
    },
    'styles.css': {},
    'table-styles.css': {}
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
        render_kwargs = RENDER_KWARGS_BY_FILENAME[filename]
        build_public(filename, render_kwargs)
