import json
import sys
from os import path

header_comment = '# %%\n'


def nb2py(notebook):
    ''' Convert a jupyter notebook to a python script string '''

    result = []
    cells = notebook['cells']

    for cell in cells:
        cell_type = cell['cell_type']

        if cell_type == 'markdown':
            result.append("%s'''\n%s\n'''" %
                          (header_comment, ''.join(cell['source'])))

        if cell_type == 'code':
            result.append("%s%s" % (header_comment, ''.join(cell['source'])))

    return '\n\n'.join(result)



def py2nb(py_str):
    ''' Convert a python script to a jupyter notebook string '''

    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment):]

    cells = []
    chunks = py_str.split('\n\n%s' % header_comment)

    for chunk in chunks:
        cell_type = 'code'
        
        if chunk.startswith("'''"):
            chunk = chunk.strip("'\n")
            cell_type = 'markdown'

        cell = {
            'cell_type': cell_type,
            'metadata': {},
            'source': chunk.splitlines(True),
        }

        if cell_type == 'code':
            cell.update({'outputs': [], 'execution_count': None})

        cells.append(cell)

    notebook = {
        'cells': cells,
        'metadata': {
            'anaconda-cloud': {},
            'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'},
            'language_info': {
                'codemirror_mode': {'name': 'ipython', 'version': 3},
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.6.1'
                }
            },
        'nbformat': 4,
        'nbformat_minor': 1
    }

    return notebook


def convert(in_file, out_file):
    _, in_ext = path.splitext(in_file)
    _, out_ext = path.splitext(out_file)

    if in_ext == '.ipynb' and out_ext == '.py':
        with open(in_file, 'r') as f:
            notebook = json.load(f)

        with open(out_file, 'w') as f:
            f.write(nb2py(notebook))

    elif in_ext == '.py' and out_ext == '.ipynb':
        with open(in_file, 'r') as f:
            py_str = f.read()

        with open(out_file, 'w') as f:
            json.dump(py2nb(py_str), f, indent=2)

    else:
        raise(Exception('Extensions must be .ipynb and .py or vice versa'))



if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 3:
        print('Usage: python -m pyfileconverter in.ipynb out.py')
        print('or:    python -m pyfileconverter in.py out.ipynb')
        sys.exit(1)

    convert(in_file=argv[1], out_file=argv[2])
