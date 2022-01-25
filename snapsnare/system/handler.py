import logging
import os
import snapsnare

from dataclasses import dataclass
from pathlib import Path
from paprika_connector.connectors.connector_factory import ConnectorFactory
from snapsnare.repositories.log.log_repository import LogRepository
from snapsnare.system import utils


@dataclass
class LogData:
    uuid: str = None,
    name: str = None,
    msg: str = None,
    args: str = None,
    levelname: str = None,
    levelno: int = None,
    pathname: str = None,
    filename: str = None,
    module: str = None,
    exc_info: str = None,
    exc_text: str = None,
    stack_info: str = None,
    lineno: int = None,
    funcName: str = None,
    created: float = None,
    msecs: float = None,
    relativeCreated: float = None,
    thread: int = None,
    threadName: str = None,
    processName: str = None,
    process: int = None,
    message: str = None,
    asctime: str = None,

    def __init__(self, record: logging.LogRecord):
        for key in record.__dict__:
            if isinstance(record.__dict__[key], tuple):
                self.__setattr__(key, record.__dict__[key].__str__())
            else:
                self.__setattr__(key, record.__dict__[key])


class LogDBHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

        properties = {
            'current.dir': os.path.abspath(os.getcwd()),
            'package.dir': os.path.dirname(snapsnare.__file__),
            'home.dir': str(Path.home()),
            'app.name': 'snapsnare'
        }

        ds = utils.load_json(properties, 'snapsnare-ds.json')
        self.__connector = ConnectorFactory.create_connector(ds)

    def get_connector(self):
        return self.__connector

    def emit(self, record):
        try:
            connector = self.get_connector()
            log_repository = LogRepository(connector)
            log_repository.insert(LogData(record).__dict__)
            connector.commit()
        except Exception:
            if record:
                print(f"{record=}")

        # todo, recursive logging due to log statement in paprika-connector, in loglevel DEBUG
