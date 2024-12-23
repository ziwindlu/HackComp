import logging

logging.basicConfig(
    level=logging.DEBUG,  # 设置全局日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置时间格式
    # filename='app.log',  # 设置日志文件路径（不需要文件输出可省略此行）
    # filemode='a',  # 设置文件模式为追加模式（默认是 'a'）
)

log = logging.getLogger(__name__)