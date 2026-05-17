from __future__ import absolute_import

import sys

from logging import Logger, StreamHandler


def patch():
    import logging
    from .formatter import ExceptionFormatter, THEME, MAX_LENGTH, PIPE_CHAR, CAP_CHAR

    def logging_format_exception(exc_info):
        formatter = ExceptionFormatter(
            colored=False, theme=THEME, max_length=MAX_LENGTH,
            pipe_char=PIPE_CHAR, cap_char=CAP_CHAR
        )
        return u''.join(formatter.format_exception(*exc_info))

    if hasattr(logging, '_defaultFormatter'):
        logging._defaultFormatter.format_exception = logging_format_exception

    patchables = [handler() for handler in logging._handlerList if isinstance(handler(), StreamHandler)]
    patchables = [handler for handler in patchables if handler.stream == sys.stderr]
    patchables = [handler for handler in patchables if handler.formatter is not None]
    for handler in patchables:
        handler.formatter.formatException = logging_format_exception


class BetExcLogger(Logger):
    def __init__(self, *args, **kwargs):
        super(BetExcLogger, self).__init__(*args, **kwargs)
        patch()
