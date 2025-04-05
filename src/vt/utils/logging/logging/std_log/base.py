#!/usr/bin/env python3
# coding=utf-8

"""
Logging interfaces for the standard logging library of python.
"""
from abc import abstractmethod
from logging import Logger, addLevelName, getLevelNamesMapping
from typing import Protocol, Any, Mapping, override

from vt.utils.logging.logging import MinLogProtocol, AllLevelLogger
from vt.utils.logging.logging.base import FatalLogProtocol, ExceptionLogProtocol, HasUnderlyingLogger
from vt.utils.logging.logging.std_log import TRACE_LOG_LEVEL, TRACE_LOG_STR, SUCCESS_LOG_LEVEL, SUCCESS_LOG_STR, \
    NOTICE_LOG_LEVEL, NOTICE_LOG_STR, EXCEPTION_TRACEBACK_LOG_LEVEL, EXCEPTION_TRACEBACK_LOG_STR, FATAL_LOG_LEVEL, \
    FATAL_LOG_STR, CMD_LOG_LEVEL, CMD_LOG_STR


class StdLogProtocol(MinLogProtocol, Protocol):
    """
    Logger protocol that is followed (for methods) by the python std logging.

    Two additional methods are added on top of the MinLogProtocol::

        - fatal
        - exception

    along with properties that python std logger provides::

        - name
        - level
        - disabled
    """
    name: str
    level: int
    disabled: bool

    def fatal(self, msg: str, *args, **kwargs) -> None:
        ...

    # noinspection SpellCheckingInspection
    # required for the param stack-level because this method signature from the protocol needs to correctly match that
    # of the std logging method signature.
    def exception(self, msg: object, *args: object, exc_info: Any = ..., stack_info: bool = ...,
                  stacklevel: int = ..., extra: Mapping[str, object] | None = ...) -> None:
        ...


class StdLevelLogger(MinLogProtocol, FatalLogProtocol, ExceptionLogProtocol, HasUnderlyingLogger, Protocol):
    """
    Logger that implements python standard logging methods::

        - debug
        - info
        - warning
        - error
        - critical
        - fatal
        - exception
    """
    pass


class DirectStdAllLevelLogger(AllLevelLogger, Protocol):
    """
    All logging levels as provided by the python std logging.
    """
    DEFAULT_LEVEL_MAP: dict[int, str] = {TRACE_LOG_LEVEL: TRACE_LOG_STR,
                                         SUCCESS_LOG_LEVEL: SUCCESS_LOG_STR,
                                         NOTICE_LOG_LEVEL: NOTICE_LOG_STR,
                                         CMD_LOG_LEVEL: CMD_LOG_STR,
                                         EXCEPTION_TRACEBACK_LOG_LEVEL: EXCEPTION_TRACEBACK_LOG_STR,
                                         FATAL_LOG_LEVEL: FATAL_LOG_STR}
    """
    All log levels in accordance with the python std log. Ordered in such a fashion::
    
        3 -> TRACEBACK
        5 -> TRACE
        10 -> DEBUG
        20 -> INFO
        23 -> SUCCESS
        26 -> NOTICE
        28 -> CMD-CALL
        30 -> WARNING
        40 -> ERROR
        50 -> CRITICAL
        60 -> FATAL
    """

    @staticmethod
    def register_levels(level_name_map: dict[int, str] | None = None) -> dict[int, str]:
        """
        Register levels in the python std logger.

        Note::

            The level changes are global in python std library hence, multiple calls to
            ``DirectStdAllLevelLogger.register_levels()`` may result in the latest call to win.

        :param level_name_map: log level - name mapping. This mapping updates the
            ``DirectStdAllLevelLogger.DEFAULT_LEVEL_MAP`` and then all the updated
            ``DirectStdAllLevelLogger.DEFAULT_LEVEL_MAP`` log levels are registered.
        :return: An ascending sorted level -> name map of all the registered log levels.
        """
        if level_name_map:
            DirectStdAllLevelLogger.DEFAULT_LEVEL_MAP.update(level_name_map)
        for level in DirectStdAllLevelLogger.DEFAULT_LEVEL_MAP:
            addLevelName(level, DirectStdAllLevelLogger.DEFAULT_LEVEL_MAP[level])
        return {l: n for n, l in sorted(getLevelNamesMapping().items(), key=lambda name_level: name_level[1])}

    @override
    @property
    @abstractmethod
    def underlying_logger(self) -> Logger: # noqa
        pass
