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


unsafe_words = [
    ';', '|', '&', '$', '>', '<', '`', '${', '$('
]


def escape_in_quotes_text(line: str, quotes: str):
    if quotes == '"':
        return line.replace('"', '\\"')
    elif quotes == "'":
        return line.replace('\'', '\\\'')


def escape_unsafe_text(text):
    for word in unsafe_words:
        text = text.replace(word, f'\\{word}')
    return text


def has_unsafe_words(line: str) -> bool:
    global unsafe_words
    for word in unsafe_words:
        if word in line:
            return True
    return False


def check_and_escape_text(text: str) -> str:
    if has_unsafe_words(text):
        return escape_unsafe_text(text)
    return text
