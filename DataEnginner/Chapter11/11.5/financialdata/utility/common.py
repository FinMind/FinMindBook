import datetime
import typing


def get_today(
    string: bool = True,
) -> typing.Union[str, datetime.date]:
    today = (
        datetime.datetime.utcnow()
        + datetime.timedelta(hours=8)
    ).date()
    if string:
        return today.strftime(
            "%Y-%m-%d"
        )
    else:
        return today
