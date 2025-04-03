#!/usr/bin/env python3
# coding=utf-8


"""
Logger interfaces for Logger formatters.
"""


from abc import abstractmethod
from typing import Protocol, TextIO


class LogLevelFmt(Protocol):
    @abstractmethod
    def fmt(self, level: int) -> str:
        pass


class AllLevelSameFmt(LogLevelFmt, Protocol):
    pass


class DiffLevelDiffFmt(LogLevelFmt, Protocol):
    @abstractmethod
    def next_approx_level(self, missing_level: int) -> int:
        pass


class StreamFormatMapper(Protocol):
    @property
    @abstractmethod
    def stream_fmt_map(self) -> dict[TextIO, LogLevelFmt]:
        ...

    @abstractmethod
    def fmt_handler(self, stream: TextIO) -> LogLevelFmt:
        pass
