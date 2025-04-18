#!/usr/bin/env python3
# coding=utf-8

"""
Important utilities for std python logging library.
"""
import logging
import warnings

from vt.utils.logging.warnings import suppress_warning_stacktrace


def level_name_mapping() -> dict[int, str]:
    """
    :return: level -> name mapping from std lib.
    """
    return {level: logging.getLevelName(level) for level in
            sorted(logging.getLevelNamesMapping().values())}


class TempSetLevelName:
    def __init__(self, level: int, level_name: str | None, reverting_lvl_name: str, no_warn: bool = False):
        """
        Set the log level name temporarily and then revert it back to the ``reverting_lvl_name``.

        :param level: The log level to set name to.
        :param level_name: Level name to set the level to.
        :param reverting_lvl_name: The log level name to revert to when operation finishes.
        :param no_warn: A warning is shown if the supplied ``level_name`` is strip-empty. This warning can be suppressed
            by setting ``no_warn=True``.
        """
        self.level = level
        self.level_name = level_name
        self.reverting_lvl_name = reverting_lvl_name
        self.no_warn = no_warn
        self.original_level_name = logging.getLevelName(level)

    def __enter__(self):
        if self.level_name is not None:
            if self.level_name.strip() == '':
                self.warn_user()
            else:
                logging.addLevelName(self.level, self.level_name)

    def warn_user(self):
        """
        A warning is shown if the supplied ``level_name`` is strip-empty. This warning can be suppressed
            by setting ``no_warn=True`` in ctor.
        """
        if not self.no_warn:
            with suppress_warning_stacktrace():
                self._warn_user()

    def _warn_user(self):
        warnings.warn(f"Supplied log level name for log level {self.level} is empty.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.level_name:
            logging.addLevelName(self.level, self.reverting_lvl_name)
        else:
            logging.addLevelName(self.level, self.original_level_name)
