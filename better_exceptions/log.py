from __future__ import absolute_import

import logging
import sys

from logging import Logger, StreamHandler


def _uncolored_format_exception(exc_info):
    """Format exception without ANSI color codes."""
    from .formatter import ExceptionFormatter, THEME, MAX_LENGTH, PIPE_CHAR, CAP_CHAR

    formatter = ExceptionFormatter(
        colored=False, theme=THEME, max_length=MAX_LENGTH,
        pipe_char=PIPE_CHAR, cap_char=CAP_CHAR
    )
    return u''.join(formatter.format_exception(*exc_info))


def patch():
    from . import format_exception

    colored_fn = lambda exc_info: u''.join(format_exception(*exc_info))

    for handler_ref in logging._handlerList:
        handler = handler_ref()
        if handler is None or handler.formatter is None:
            continue

        if isinstance(handler, StreamHandler) and handler.stream is sys.stderr:
            handler.formatter.formatException = colored_fn
        else:
            handler.formatter.formatException = _uncolored_format_exception


class BetExcLogger(Logger):
    def __init__(self, *args, **kwargs):
        super(BetExcLogger, self).__init__(*args, **kwargs)
        patch()
