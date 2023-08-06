from loguru import logger
import configparser

name = "kordar_task"

config = configparser.ConfigParser()
config.read("kordar_task.ini")

logger.add(config['logger']['filename'],
           enqueue=True,
           level=config['logger']['level'],
           rotation=config['logger']['rotation'],
           encoding=config['logger']['encoding']
           )


def write_logger(msg, t="info"):
    if t == "info":
        logger.info(msg)
    elif t == "error":
        logger.error(msg)
    elif t == "warning":
        logger.warning(msg)
