from meutils.pipe import *
from meutils.log_utils import logger4feishu


def job(packages="meutils[plus] cloud-ml-sdk", pip='pip', is_test=False):
    """

    :param packages: 开个分割
    :param pip:
    :return:
    """
    cmd = f"""
    {pip} install -U --no-cache-dir -i https://mirror.baidu.com/pypi/simple {packages} 
    && {pip} install -U --no-cache-dir -i https://pypi.python.org/pypi {packages}
    """

    status, output = magic_cmd(cmd)
    output = output | xjoin
    if ('Successfully installed' in output) | is_test:
        update_info = output.split()[-1]

        cmd = "cloudml dev save_v2 -f cpu666 me"
        save_info = magic_cmd(cmd)[1] | xjoin

        logger4feishu('CM镜像更新', f"更新: {update_info}\n{save_info}")


    else:
        logger.info('无更新')


# 初始化
job(is_test=True)
# schedule.every(15).minutes.do(job)
#
# if __name__ == '__main__':
#
#     while True:
#         schedule.run_pending()
