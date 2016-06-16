import logging
import os

def checked(name):
    if not os.path.exists(name):
        os.mkdir(name)
    return name

def getFileLogger(name,filename=None,log_level=logging.INFO):
    if filename is None:
        filename = "%s.log" % name
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)

    file_handler = logging.FileHandler(filename, 'a+')
    file_handler.level = log_level
    logger.addHandler(file_handler)

    #test
    logger.debug('this is debug message')
    logger.info('this is info message')
    logger.warning('this is warning message')
    logger.error('this is error message')
    logger.critical('this is critical message')

    return logger