import os

import shutil

from collections import defaultdict

from admin.models import JWT, Restricted_by_JWT, Relationship

from templates.models import metadata


DOCS_THEME = {
    'h1': {
        'font-family': 'serif',
        'color': '#4b1b4b',
        'text-align': 'center',
        'font-size': '50px'
    },
    'h2': {
        'font-family': 'serif',
        'color': '#08001a',
        'text-align': 'justify',
        'font-size': '25px'
    },
    'h3': {
        'font-family': 'serif',
        'color': '#4b1b4b',
        'text-align': 'left',
        'font-size': '30px'
    },
    'mark_get': {
        'background-color': '#a6f0c6',
    },
    'mark_post': {
        'background-color': '#f9f871',
    },
    'mark_put': {
        'background-color': '#64dfdf',
    },
    'mark_delete': {
        'background-color': '#eb596e',
    },
    'subheading': {
        'font-family': 'cursive',
        'color': '#a278b5',
        'text-align': 'left',
        'font-size': '28px'
    },
    'p': {
        'font-family': 'verdana',
        'text-align': 'justify',
        'font-size': '20px'
    },
    'body': {
        'background-color': '#ebc7eb'
    }
}


def css_generator(placeholder, text, color, alignment, **kwargs):

    if kwargs is None:
        pass

    else:
        for placeholder, formatting in kwargs.items():
            try:
                DOCS_THEME[placeholder][formatting] = formatting
            except KeyError:
                pass


def tag_text(tag: str, text: str) -> str:
    return '<' + tag + '>' + text + '</' + tag + '>\n'


def add_body(app_name, dest, platform):

    folder = '/'.join(dest.split('/')[:-1]) + '/' + app_name
    app_type = 'Basic'
    htmlfile = open(dest, 'r+')
    content = htmlfile.readlines()
    loc = content.index('</body>\n')
    tables = []

    for name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, name)):
            tables.append(name)

    jwt_configured = JWT.query.filter_by(
                                        connection_name=app_name
                                        ).first()
    restricted_tables = Restricted_by_JWT.query.filter_by(
                                        connection_name=app_name
                                        ).first()

    if jwt_configured is not None:
        app_type = 'JWT Authenticated'

    tables = defaultdict(dict)
    for table in metadata.sorted_tables:
        tables[table.info['bind_key']][table.name] = table

    tables = tables[app_name]

    for level in DOCS_THEME.keys():
        info = ['<' + level + '>']

        if level == 'h1':
            if platform == 'local':
                info.append(app_name.title() + ': ' + app_type + ' API Docs')
        if level == 'h2':
            if app_type == 'JWT Authenticated':
                base_table = jwt_configured.table
                if restricted_tables is not None:
                    locked_tables = restricted_tables.restricted_tables \
                                   .split(',')
                info.append('The docs cover the endpoints available, ' +
                            'table-wise as well as relationships if any were' +
                            'defined.' +
                            'The app provides the user with a base table ' +
                            base_table)
                tables.remove(base_table)

            if len(tables) != 0:
                info.append('The app provides public assess to the'
                            ' following tables :\n')
                table_info = ''

                if len(tables.keys()) > 0:
                    for i in tables.keys():
                        table_info += tag_text('li', i + '\n')
                table_info = tag_text('ol', table_info)
                info.append(table_info)
            else:
                tag_text('mark', 'No Public Tables')
        if level == 'h3':
            # document base JWT
            if app_type == 'JWT Authenticated':
                info.append('Base table for authenticating users: ' +
                            base_table)
                table_obj = tables[base_table]
                para_text = 'Table ' + table_obj.name + \
                            ' is the base table' + \
                            ' that will be used track the registered users' + \
                            ' the following API endpoints have been ' + \
                            'configured:\n'

                filter_keys = table_obj.filter_keys.split(',')
                for column in tables.columns:
                    pass
            if app_type == 'Basic':
                para_text = 'This app gives unrestricted access to access' + \
                            ' edit, populate and remove values from the ' + \
                            'connected tables.\n'
            # doccument the rest of the tables

        else:
            info.append('<br>' + level)

        info.append('</' + level + '>\n')
        content[loc:loc] = info
        loc = loc + len(info)

        if level == 'h3':
            if para_text != '':
                para_text = tag_text('p', para_text)
                content[loc:loc] = para_text
                loc = loc + 1

    htmlfile.seek(0)
    htmlfile.write(''.join(content))


def create_docs_page(app_name, parent_dir, dest_dir) -> str:

    d = dest_dir + '/exported_app/app/docs.html'
    os.makedirs(os.path.dirname(d), exist_ok=True)

    shutil.copy(parent_dir + '/templates/export/docs.html', d)
    return d


def create_stylesheet(dest, **kwargs):

    f = open(dest, 'r+')
    lines = f.readlines()
    style = []

    for element, description in DOCS_THEME.items():
        style.append(element + ' {\n')
        for key, value in description.items():
            style.append(key + ': ' + value + ';\n')
        style.append('}\n')

    lines[4:4] = style
    f.seek(0)
    for line in lines:
        f.write(line)
