import re
from common import *
from collections import Counter

# 默认的猜测索引占比值
guss_index_proportion = 0.5


class SubCommand:
    def __init__(self, name: str, desc: str):
        self.name = name
        self.desc = desc


class Option:
    def __init__(self, name: str, desc: str):
        self.name: str = name
        self.desc: str = desc


class Resolve:
    def __init__(self, cmd_name: str):
        self.cmd_name = cmd_name
        self.options = []
        self.subcommands = []
        self.reg_cmd = cmd_name


def resolve_subcommand(args: dict, help_list: List[str]) -> List[SubCommand]:
    # todo
    pass


def resolve_options(args: dict, help_list: List[str]) -> List[Option]:
    if 'desc_index' in args:
        # todo 后面要改，这里没做具体实现
        n = args.get('desc_index')
        name_index = n
        desc_index = n
    else:
        name_index, desc_index = guss_option_index(help_list)
    log.debug(f"resolve_option: name_index: {name_index}, desc_index: {desc_index}")
    result_list = []
    option_name_list = []
    option_desc_list = []
    # 解析出option name与desc
    for line in help_list:
        # -开头认为是option name
        if line[name_index:desc_index].startswith('-'):
            # 判断是否存在"  "，如果没有说明该option name为单独一行
            if line.strip().find("  ") > 0:
                log.debug(f"resolve_option: find new option. line: ' {line} '")
                option_name_list.append(line[:desc_index].strip())
                option_desc_list.append([line[desc_index:].strip()])
            else:
                log.debug(f"resolve_option: find new name. line: ' {line} '")
                option_name_list.append(line.strip())
                option_desc_list.append([])
        else:
            # 如果前面全是空，直到desc_index重合 则认为是上一个option的desc
            if len(line) - len(line.lstrip()) == desc_index:
                log.debug(f"resolve_option: find new desc. line: ' {line} '")
                option_desc_list[len(option_desc_list) - 1].append(line.strip())
            else:
                log.debug(f"resolve_option: line: ' {line} ' is not option")
    for index, name in enumerate(option_name_list, 0):
        option = Option(name, ''.join(option_desc_list[index]))
        result_list.append(option)
    return result_list


def get_help_resolve(args: dict, help_content: str) -> Resolve:
    # 获取命令名
    cmd_name = get_cmd_name(help_content=help_content)
    r = Resolve(cmd_name)
    help_list = split_help_content(help_content=help_content)
    # 解析subcommand
    subcommands = resolve_subcommand(args, help_list)
    # 解析option
    options = resolve_options(args, help_list)
    r.subcommands = subcommands
    r.options = options
    return r


def split_help_content(help_content: str) -> List[str]:
    return help_content.split('\n')


def percent_of_list(c: int, l: list):
    return c / len(l)


def get_most_common_number_by_counter(data_list: List[int]):
    option_name_counter = Counter(data_list)
    # 获取出现次数最多的元素
    most_option_name_common = option_name_counter.most_common(1)
    # 看看出现次数是否超过一半
    if percent_of_list(most_option_name_common[0][1], data_list) > guss_index_proportion:
        return most_option_name_common[0][0]
    else:
        return None


def guss_option_index(help_list: List[str]):
    # 如果不好用，后面要添加用户传入的辅助index
    filtered_list = filter(lambda x: '-' in x, help_list)
    option_name_indexes = []
    option_desc_indexes = []
    for line in filtered_list:
        l_line = line.lstrip()
        # 获取option名称的索引
        option_name_index = len(line) - len(l_line)
        option_name_indexes.append(option_name_index)
        # 获取option描述的索引
        # 我们认为存在两个空格的位置为name与desc之间的空白的开始，我们截取空白之后的位置，获取描述的索引
        # 如果没有，则跳过
        blank_start_index = l_line.find("  ")
        if blank_start_index < 0:
            option_desc_indexes.append(blank_start_index)
        else:
            no_option_name_str = l_line[blank_start_index:]
            option_desc_indexes.append(len(line) - len(no_option_name_str.lstrip()))
    # 开始统计
    real_option_name_index = get_most_common_number_by_counter(option_name_indexes)
    real_option_desc_index = get_most_common_number_by_counter(option_desc_indexes)
    if real_option_name_index >= 0 and real_option_desc_index >= 0:
        return real_option_name_index, real_option_desc_index
    else:
        raise Exception('resolve: guss option index failed')


def guss_subcommand_index(help_list: List[str]):
    pass


def get_cmd_name(help_content: str) -> str:
    r = r"(?i)\busage:\s+(\S+)\b.*"
    search_result = re.search(r, help_content)
    if search_result.groups():
        return search_result.groups()[0]
    else:
        raise Exception('resolve: get cmd name failed')


# test_content = """
# usage: gen_comp.py [-h] [-t TYPE] [--reg-cmd REG_CMD] [--no-strigula] [-f HELP_FILE]
#
# options:
#   -h, --help            show this help message and exit
#   -t TYPE, --type TYPE  输入类型
#   --reg-cmd REG_CMD     注册命令
#   --no-strigula         不使用-解析--help类型
#   -f HELP_FILE, --help-file HELP_FILE
#                         指定help文件
# """
# o = get_help_resolve({}, test_content)
# print(o)
