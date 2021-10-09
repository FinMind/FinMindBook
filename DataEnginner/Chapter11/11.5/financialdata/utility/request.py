import time
import typing

import requests
from loguru import logger
from tqdm import tqdm

# 避免遇到
# Max retries exceeded
# 或 Read timed out
# 以上兩種狀況
# 在 request 的部分
# 實做 retry 進行爬蟲
def get(
    url: str,
    header: typing.Dict[
        str,
        typing.Union[str, int, float],
    ] = {},
    sleep: int = 0,
    params: typing.Dict[
        str,
        typing.Union[str, int, float],
    ] = {},
    dataset: str = "",
) -> requests.models.Response:
    for i in tqdm(range(10)):
        try:
            time.sleep(sleep)
            res = requests.get(
                url,
                verify=False,
                timeout=30,
                headers=header,
                params=params,
            )
            return res
        except Exception as e:
            logger.info(e)
            if (
                "Max retries exceeded"
                in str(e)
                or "Read timed out"
                in str(e)
            ):
                time.sleep(30)
            else:
                raise Exception(str(e))
            if i == 9:
                raise Exception(str(e))


def post(
    url: str,
    header: typing.Dict[
        str,
        typing.Union[str, int, float],
    ],
    form_data: typing.Dict[
        str,
        typing.Union[str, int, float],
    ],
    sleep: int = 0,
    dataset: str = "",
) -> requests.models.Response:
    for i in tqdm(range(10)):
        try:
            time.sleep(sleep)
            res = requests.post(
                url,
                verify=False,
                timeout=30,
                headers=header,
                data=form_data,
            )
            return res
        except Exception as e:
            logger.info(e)
            if (
                "Max retries exceeded"
                in str(e)
                or "Read timed out"
                in str(e)
            ):
                time.sleep(30)
            else:
                raise Exception(str(e))
            if i == 9:
                raise Exception(str(e))
