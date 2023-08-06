import time
from loguru import logger


def timeit(func):
    """
    :param func: 需要传入的函数
    :return:
    """

    def _warp(*args, **kwargs):
        """
        :param args: func需要的位置参数
        :param kwargs: func需要的关键字参数
        :return: 函数的执行结果
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        changed_time = time.time() - start_time
        logger.info(f'{func.__name__} 用时：{changed_time:.2f}s')
        return result

    return _warp
