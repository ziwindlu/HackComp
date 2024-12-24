import argparse
import os.path

from common import *
from help_resolve import *
from jinja2 import Template

current_config: argparse.Namespace = argparse.Namespace()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=str, default='help', help='输入类型')
    parser.add_argument('--reg-cmd', type=str, help='注册命令')
    parser.add_argument('--no-strigula', action='store_true', help='不使用-解析--help类型')
    parser.add_argument('-f', '--help-file', type=str, help='指定help文件')
    parser.add_argument('--output-dir', type=str, default='output', help='输出到某个文件夹')
    return parser.parse_args()


def bash_arg_preprocess(args):
    str_list = ''
    for k in args['options']:
        str_list += f"{k.name} "
    args['total_options_list'] = str_list
    return args


def zsh_arg_preprocess(args):
    # 命令名转义
    args['reg_cmd'] = template_util.escape_reg_cmd(args['reg_cmd'])
    # 存在name为"-a --abc"的option需要重新分割，顺序打乱了
    no_preprocess_options = [o for o in args['options'] if ',' not in o.name]
    need_preprocess_options = [o for o in args['options'] if ',' in o.name]
    for need in need_preprocess_options:
        split_names = need.name.split(',')
        for s in split_names:
            if s.strip().startswith('-'):
                no_preprocess_options.append(Option(s.strip(), need.desc))
    # 描述转义，描述中存在[]会导致无法补全
    for o in no_preprocess_options:
        o.desc = o.desc.replace('[', '\\[').replace(']', '\\]')
    args['options'] = no_preprocess_options
    return args


def bash_arg_after_process(rendered_template: str, args):
    f_p = f'{args["cmd_name"]}.bash'
    if current_config.output_dir:
        f_p = os.path.join(current_config.output_dir, f_p)
    file_util.write_file_auto_check(f_p, rendered_template)
    template_util.rm_empty_lines(f_p)
    return True


def zsh_arg_after_process(rendered_template: str, args):
    f_p = f'{args["cmd_name"]}.zsh'
    if current_config.output_dir:
        f_p = os.path.join(current_config.output_dir, f_p)
    file_util.write_file_auto_check(f_p, rendered_template)
    template_util.rm_empty_lines(f_p)
    return True


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


def get_help_args(template_type: str, help_content: str) -> Resolve:
    result: Resolve
    log.debug(f'get args')
    if template_type == 'bash' or template_type == 'zsh':
        result = get_help_resolve(current_config.__dict__, help_content)
        log.debug(f'get args done')
        return result
    log.error(f'get args failed: {template_type}')
    sys.exit(1)


def gen_comp(template_type: str, args: Resolve):
    template: Template
    try:
        log.debug(f'get {template_type} template')
        template = template_util.get_template(f'{template_type}_comp_template')
        log.debug(f'get {template_type} template done')
    except Exception as e:
        log.error(f'get {template_type} template failed: {e}')
        sys.exit(1)
    this_args = args.__dict__
    log.debug(f'get {template_type} args done')
    run_fn_by_type_preprocess(template_type=template_type, args=this_args)
    log.debug(f'render {template_type} template')
    rendered_content = template.render(**this_args)
    log.debug(f'render {template_type} template done')
    run_fn_by_type_after_process(template_type=template_type, rendered_template=rendered_content, args=this_args)


def init():
    global current_config
    current_config = get_args()


def run(comp_type: str, file_content: str):
    help_args = get_help_args(comp_type, help_content=file_content)
    gen_comp(comp_type, args=help_args)


if __name__ == '__main__':
    init()
    content4help = file_util.read_file(current_config.help_file)
    types = ['bash', 'zsh']
    for t in types:
        run(t, content4help)
