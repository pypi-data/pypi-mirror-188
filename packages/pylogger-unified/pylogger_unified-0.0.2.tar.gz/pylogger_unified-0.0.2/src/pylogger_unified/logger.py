#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import http.client as http_client
import ast
import json
import logging
import logging.handlers
import re
import socket
import types
installed_gi = False
try:
    import gi.repository
    gi.require_version("Notify", "0.7")
    from gi.repository import Notify
    installed_gi = True
except ImportError:
    pass
except ValueError:
    pass


class CustomColorFormatter(logging.Formatter):

    color_levels = {
        "DEBUG": "\033[0;34;21m\033[24m" + "%(category)s - %(message)s" + "\033[1;37;0m",
        "INFO": "\033[0;32;21m\033[24m" + "%(category)s - %(message)s" + "\033[1;37;0m",
        "WARNING": "\033[1;33;21m\033[24m" + "%(category)s - %(message)s" + "\033[1;37;0m",
        "ERROR": "\033[1;31;21m\033[24m" + "%(category)s - %(message)s" + "\033[1;37;0m",
        "CRITICAL": "\033[1;31;21m\033[24m" + "%(category)s - %(message)s" + "\033[1;37;0m"
    }

    gi_levels = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 1,
        "ERROR": 2,
        "CRITICAL": 2,
    }

    def __init__(self, category="main", has_gi=False):
        super().__init__()
        self.category = category
        self.has_gi = has_gi
        if has_gi:
            Notify.init(category)
            self.gnotify = Notify.Notification.new("")
            self.gnotify.set_urgency(2)

    def format(self, record):
        if self.has_gi:
            self.gnotify.set_urgency(self.gi_levels[record.levelname])
            self.gnotify.update(self.category, record.getMessage())
            self.gnotify.show()
        record.category = self.category
        formatter = logging.Formatter(self.color_levels[record.levelname])
        return formatter.format(record)


class CustomJsonFormatter(logging.Formatter):  # pylint: disable=too-few-public-methods

    graylog_levels = {
        "DEBUG": 7,
        "INFO": 6,
        "WARNING": 4,
        "ERROR": 3,
        "CRITICAL": 2,
    }

    forbidden_attrs = (
        "args",
        "asctime",
        "call_ip",
        "category",
        "created",
        "exc_info",
        "exc_text",
        "facility",
        "file",
        "filename",
        "full_message",
        "funcName",
        "host",
        "id",
        "ip",
        "level",
        "levelname",
        "levelno",
        "line",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "region",
        "relativeCreated",
        "short_message",
        "stack_info",
        "tag",
        "thread",
        "threadName",
        "timestamp",
        "version"
    )

    def __init__(self, category="main", region="unknown", is_http=False, extra=None):
        if extra is None:
            extra = {}
        super().__init__()
        self.hostname = socket.gethostname()
        self.category = category
        self.region = region
        self.is_http = is_http
        self.extra = extra

    def format(self, record):
        log_record = {
            "version": "1.1",
            "host": self.hostname,
            "short_message": record.getMessage(),
            "timestamp": record.created,
            "level": self.graylog_levels[record.levelname],
            "_category": self.category,
            "_region": self.region
        }
        if self.is_http:
            match = re.compile(r'^(.+)\s(POST|GET|PUT|DELETE)\s(\S+)\s\((\d+)\)$').match(record.getMessage())
            if match:
                try:
                    ip, call_method, call_url, call_status_int = match.groups()  # pylint: disable=unused-variable
                    log_record["_call_source"] = ip
                    log_record["_call_method"] = call_method
                    log_record["_call_url"] = call_url
                    log_record["_call_status_int"] = call_status_int
                except ValueError:
                    pass
        if record.exc_info is not None:
            log_record["full_message"] = self.formatException(record.exc_info)
        record.asctime = self.formatTime(record)
        for key, value in {**record.__dict__, **self.extra}.items():
            new_key = re.sub(r'^_+', "", key)
            if new_key not in self.forbidden_attrs:
                new_key = "_" + key
                try:
                    json.dumps(value)
                except (TypeError, OverflowError):
                    # If value is not JSON serializable
                    # convert to string
                    log_record[new_key] = str(value)
                else:
                    # If value is JSON serializable,
                    # value will be encoded in the following return
                    log_record[new_key] = value
        return json.dumps(log_record)


class CustomFlaskFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    http_levels = {
        "5xx": {
            "levelname": "CRITICAL",
            "levelno": 50
        },
        "4xx": {
            "levelname": "ERROR",
            "levelno": 40
        },
        "3xx": {
            "levelname": "WARNING",
            "levelno": 30
        },
        "2xx": {
            "levelname": "INFO",
            "levelno": 20
        },
        "1xx": {
            "levelname": "DEBUG",
            "levelno": 10
        }
    }

    @classmethod
    def http_status_to_log_level(cls, status_code=500):
        if status_code >= 500:
            status_range = "5xx"
        elif status_code >= 400:
            status_range = "4xx"
        elif status_code >= 300:
            status_range = "3xx"
        elif status_code >= 200:
            status_range = "2xx"
        else:
            status_range = "1xx"
        return cls.http_levels[status_range]["levelname"], cls.http_levels[status_range]["levelno"]

    def filter(self, record):
        match = re.compile(r'^(.*?) - - \[(.*?)\] "(.*?) (.*?) (.*?)" (\d+) (\d+) "-" "(.*?)"$').match(record.msg)
        if match:
            try:
                ip, date, call_method, call_url, http_version, status_code, size, http_agent = match.groups()  # pylint: disable=unused-variable
                request_line = call_method + " " + call_url
                record.msg = ip + " " + request_line + " (" + status_code + ")"
                try:
                    record.levelname, record.levelno = self.http_status_to_log_level(status_code=int(status_code))
                except ValueError:
                    pass
            except ValueError:
                pass
            return record


# functions


def pretty(self, msg, no_debug=False, *args, **kwargs):
    level = 10
    if no_debug:
        level = 20
    try:
        msg.__dict__
        msg = complex_obj_to_dict(msg)
    except:
        pass
    msg = json.dumps(
        msg,
        indent=2,
        sort_keys=True
    )
    self.log(
        level,
        msg
    )


def complex_obj_to_dict(obj):
    if obj is None:
        return None
    try:
        obj = dict(obj)
    except:
        pass
    try:
        obj = obj.__dict__
    except:
        pass
    data = {}
    for attr, value in obj.items():
        is_none = False
        try:
            ast.literal_eval(str(value))
            if ast.literal_eval(str(value)) is None:
                is_none = True
        except:
            pass
        is_int = False
        try:
            int(value)
            is_int = True
        except:
            pass
        is_float = False
        try:
            float(value)
            is_float = True
        except:
            pass
        if is_none:
            data[attr] = None
        elif is_int:
            data[attr] = int(value)
        elif is_float:
            data[attr] = float(value)
        elif str(value).lower() == "true":
            data[attr] = True
        elif str(value).lower() == "false":
            data[attr] = False
        elif isinstance(value, str):
            data[attr] = str(value)
        # elif isinstance(value, (list, tuple, dict)) or re.compile(r"^<class 'requests.*").match(str(type(value))):
        else:
            data[attr] = complex_obj_to_dict(value)
    return data


def hide_lib_loggers(included_loggers=None, excluded_loggers=None, debug=False):
    # clear all lib related loggers except logger names provided as argument
    if debug:
        return
    if included_loggers is None:
        included_loggers = logging.root.manager.loggerDict
    if excluded_loggers is None:
        excluded_loggers = []
    for logger_name in included_loggers:
        if logging.getLogger(logger_name).getEffectiveLevel() != logging.WARNING and logger_name not in excluded_loggers:
            logging.getLogger(logger_name).setLevel(logging.WARNING)


def init_logger(json_formatter=True, flask_logging=False, enable_gi=None, format_color=True, debug=False, log_path=None, logger_name="main", region="unknown", extra=None):
    has_gi = False
    if installed_gi and (enable_gi is None or enable_gi is True):
        has_gi = True
    if extra is None:
        extra = {}
    default_level = logging.INFO
    if debug:
        default_level = logging.DEBUG
    logger = logging.getLogger(logger_name)
    logger.propagate = False

    logger.setLevel(default_level)
    if flask_logging:
        logger2 = logging.getLogger("wsgi")
        logger2.setLevel(default_level)
        logger2.addFilter(CustomFlaskFilter())  # is used by the logger, not by the handler
        logger2.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(default_level)
    if flask_logging:
        console_handler2 = logging.StreamHandler()
        console_handler2.setLevel(default_level)
    if json_formatter:
        console_handler.setFormatter(CustomJsonFormatter(category=logger_name, region=region, extra=extra))
        if flask_logging:
            console_handler2.setFormatter(CustomJsonFormatter(category="flask-" + logger_name, region=region, is_http=True, extra=extra))
    elif format_color:
        console_handler.setFormatter(CustomColorFormatter(category=logger_name, has_gi=has_gi))
        if flask_logging:
            console_handler2.setFormatter(CustomColorFormatter(category="flask-" + logger_name))

    logger_has_handler = logger.hasHandlers()
    logger2_has_handler = logger_has_handler
    if flask_logging:
        logger2_has_handler = logger2.hasHandlers()

    if not logger_has_handler:
        logger.addHandler(console_handler)
    if flask_logging and not logger2_has_handler:
        logger2.addHandler(console_handler2)  # pylint: disable=no-member

    if log_path is not None and not json_formatter:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(default_level)
        category = logger_name
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(category)s - %(levelname)s - %(message)s"))

        if not logger_has_handler:
            logger.addHandler(file_handler)
        if flask_logging and not logger2_has_handler:
            logger2.addHandler(file_handler)  # pylint: disable=no-member

    logger.pretty = types.MethodType(pretty, logger)

    return logger
