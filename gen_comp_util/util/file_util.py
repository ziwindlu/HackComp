from .log_util import log
import os.path


def file_exists(file_path: str) -> bool:
    log.debug(f'check file {file_path}')
    return os.path.exists(file_path)


def overwrite_confirm(file_path: str, confirm_txt: str = 'already exists, overwrite? (y/n)') -> bool:
    """
    覆盖写文件时的确认方法
    :param file_path: 文件路径
    :param confirm_txt: 确认时的提示
    :return: 用户确认为True,否则为False
    """
    if file_exists(file_path):
        confirm = input(confirm_txt).lower().strip()
        if confirm == 'y' or confirm == 'yes' or confirm == '':
            return True
        else:
            return False
    log.debug(f'file {file_path} not exists, return True')
    return True


def write_file(file_path: str, content: str) -> bool:
    """
    写文件
    :param file_path: 文件路径
    :param content: 文件内容
    :return: 成功True, 否则False
    """
    try:
        log.debug(f'write file {file_path}')
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        log.error(f'write file {file_path} failed: {e}')
        return False


def write_file_auto_check(file_path: str, content: str,
                          confirm_txt: str = 'already exists, overwrite? (y/n)',
                          auto_make_dir: bool = False) -> bool:
    """
    写文件，附带自动检查
    :param file_path: 路径
    :param content: 内容
    :param confirm_txt:  覆盖写时的提示
    :param auto_make_dir: 是否自动创建文件夹
    :return: 创建成功True, 否则False
    """
    f_p = os.path.realpath(file_path)
    d_p = os.path.dirname(f_p)
    # 判断文件夹是否存在
    if not file_exists(d_p):
        log.debug(f'dir {d_p} not exists')
        if not auto_make_dir:
            log.debug('auto make dir disabled, give up write file')
            return False
        log.info(f'make dir {d_p}')
        os.makedirs(d_p)
        log.debug(f'dir {d_p} created')
    else:
        log.debug(f'dir {d_p} exists')
    # 确认是否覆盖写
    if overwrite_confirm(file_path, confirm_txt):
        return write_file(file_path, content)
    else:
        log.debug('user cancel')
        return False


def read_file(file_path: str) -> str:
    """
    读取文件
    :param file_path: 文件路径
    :return: 文件内容
    """
    try:
        log.debug(f'read file {file_path}')
        if not file_exists(file_path):
            raise FileNotFoundError(f'file {file_path} not exists')
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        log.error(f'read file {file_path} failed: {e}')
