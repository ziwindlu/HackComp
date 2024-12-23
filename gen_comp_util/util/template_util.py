import os.path

from jinja2 import Template


def get_template(template_name: str) -> Template:
    p = os.path.join('./template', f'{template_name}.jinja2')
    p = os.path.realpath(p)
    with open(p, 'r') as f:
        return Template(f.read(), autoescape=True)


def rm_empty_lines(file_path: str):
    with open(file_path, 'r') as f_in:
        lines = [line for line in f_in if line.strip()]
    with open(file_path, 'w') as f_out:
        f_out.writelines(lines)


def escape_reg_cmd(s: str) -> str:
    return s.strip().replace(' ', '\\\\ ')
