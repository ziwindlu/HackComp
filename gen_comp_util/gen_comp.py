from common import *
from jinja2 import Template

current_config: dict


def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=str, default='help', help='输入类型')
    parser.add_argument('--no-strigula', action='store_true', help='不使用-解析--help类型')
    return parser.parse_args()


def bash_arg_preprocess(args):
    # todo 太丑了，要改
    str_list = ''
    for k in args['options']:
        str_list += f"{k['name']} "
    args['total_options_list'] = str_list
    return args


def zsh_arg_preprocess(args):
    args['reg_cmd'] = template_util.escape_reg_cmd(args['reg_cmd'])
    return args


def bash_arg_after_process(rendered_template: str, args):
    f_p = f'{args["cmd_name"]}.bash'
    file_util.write_file_auto_check(f_p, rendered_template)
    template_util.rm_empty_lines(f_p)
    return True


def zsh_arg_after_process(rendered_template: str, args):
    # todo 这个要改
    return bash_arg_after_process(rendered_template, args)


def run_fn_by_type_preprocess(template_type: str, args):
    log.debug(f'run fn by type preprocess')
    if template_type == 'bash':
        return bash_arg_preprocess(args=args)
    elif template_type == 'zsh':
        return zsh_arg_preprocess(args=args)
    log.debug(f'run fn by type preprocess done')


def run_fn_by_type_after_process(template_type: str, rendered_template: str, args):
    log.debug(f'run fn by type after process')
    if template_type == 'bash':
        return bash_arg_after_process(rendered_template, args=args)
    elif template_type == 'zsh':
        return zsh_arg_after_process(rendered_template, args=args)
    log.debug(f'run fn by type after process done')


def get_help_args(template_type: str) -> dict:
    # todo 这里要修改为从help中解析的
    result = {}
    log.debug(f'get args')
    if template_type == 'bash':
        result = {
            "cmd_name": "mycli",
            "options": [
                {
                    "name": "--help",
                    "description": "帮助"
                },
                {
                    "name": "--version",
                    "description": "版本"
                }
            ],
            "reg_cmd": "python mycli"
        }
    elif template_type == 'zsh':
        result = {
            "cmd_name": "mycli",
            "options": [
                {
                    "name": "--help",
                    "description": "帮助"
                },
                {
                    "name": "--version",
                    "description": "版本"
                }
            ],
            "reg_cmd": "python mycli"
        }
    log.debug(f'get args done')
    return result


def gen_comp(template_type: str):
    t: Template
    try:
        log.debug(f'get {template_type} template')
        t = template_util.get_template(f'{template_type}_comp_template')
        log.debug(f'get {template_type} template done')
    except Exception as e:
        log.error(f'get {template_type} template failed: {e}')
        sys.exit(1)
    this_args = get_help_args(template_type)
    log.debug(f'get {template_type} args done')
    run_fn_by_type_preprocess(template_type=template_type, args=this_args)
    log.debug(f'render {template_type} template')
    rendered_content = t.render(**this_args)
    log.debug(f'render {template_type} template done')
    run_fn_by_type_after_process(template_type=template_type, rendered_template=rendered_content, args=this_args)


def init(args):
    global current_config
    current_config = args


if __name__ == '__main__':
    init(get_args())
    gen_comp('zsh')
