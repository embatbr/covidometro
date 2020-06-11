# -*- coding: utf-8 -*-

# import json
import csv

from jinja2 import Environment, PackageLoader, select_autoescape


DATA_DIR = 'data'

FRONT_DIR = '../front'
TEMPLATES_DIR = '{}/templates'.format(FRONT_DIR)
PUBLIC_DIR = '{}/public'.format(FRONT_DIR)


FILENAMES = [
    'index.html', 'styles.css', 'table-styles.css'
]

reader = csv.DictReader(open('{}/2020-06-10.csv'.format(DATA_DIR)))

RENDER_KWARGS_BY_FILENAME = {
    'index.html': {
        'header': reader.fieldnames,
        'rows': [row for row in reader],
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
