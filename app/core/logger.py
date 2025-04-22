import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import structlog
from dotenv import load_dotenv
from structlog.processors import CallsiteParameter
from structlog.stdlib import BoundLogger
from structlog.typing import EventDict, Processor

# Load environment variables
load_dotenv()


class Logger:
    """
    Configure and setup logging with Structlog.

    Args:
        json_logs (bool, optional): Whether to log in JSON format. Defaults to False.
        log_level (str, optional): Minimum log level to display. Defaults to "INFO".
    """

    def __init__(self, json_logs: bool = False, log_level: str = "INFO"):
        self.json_logs = json_logs
        self.log_level = log_level.upper()

        self.environment = os.getenv("ENVIRONMENT", "PROD").upper()  # Default to PROD
        self.log_file_path = os.getenv(
            "LOG_FILE_PATH", self._get_default_log_file_path()
        )

    def _get_default_log_file_path(self) -> str | None:
        """
        Provides a default log file path outside the project folder.

        Returns:
            str: The default log file path.
        """
        return
        # default_log_dir = os.path.expanduser("./logs")
        # if not os.path.exists(default_log_dir):
        #     os.makedirs(default_log_dir)
        # return os.path.join(default_log_dir, "app.log")

    def _rename_event_key(self, _, __, event_dict: EventDict) -> EventDict:
        """
        Renames the 'event' key to 'message' in log entries.
        """
        event_dict["message"] = event_dict.pop("event", "")
        return event_dict

    def _drop_color_message_key(self, _, __, event_dict: EventDict) -> EventDict:
        """
        Removes the 'color_message' key from log entries.
        """
        event_dict.pop("color_message", None)
        return event_dict

    def _get_processors(self) -> list[Processor]:
        """
        Returns a list of structlog processors based on the specified configuration.
        """
        processors: list[Processor] = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.stdlib.ExtraAdder(),
            self._drop_color_message_key,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.CallsiteParameterAdder(
                [
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.LINENO,
                ],
            ),
        ]

        if self.json_logs:
            processors.append(self._rename_event_key)
            processors.append(structlog.processors.format_exc_info)

        return processors

    def _clear_uvicorn_loggers(self):
        """
        Clears the log handlers for uvicorn loggers.
        """
        for _log in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
            logging.getLogger(_log).handlers.clear()
            logging.getLogger(_log).propagate = True

    def _configure_structlog(self, processors: list[Processor]):
        """
        Configures structlog with the specified processors.
        """
        structlog.configure(
            processors=processors
            + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def _configure_logging(self, processors: list[Processor]) -> logging.Logger:
        """
        Configures logging with the specified processors based on the environment.

        Returns:
            logging.Logger: The configured root logger.
        """
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer()
                if self.json_logs
                else structlog.dev.ConsoleRenderer(colors=True),
            ],
        )

        root_logger = logging.getLogger()
        root_logger.handlers.clear()  # Clear existing handlers

        if self.environment == "DEV":
            # Console logging for development
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            root_logger.addHandler(stream_handler)
        else:
            # File logging for production
            file_handler = TimedRotatingFileHandler(
                filename=self.log_file_path,
                when="midnight",
                interval=1,
                backupCount=7,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        root_logger.setLevel(self.log_level.upper())
        return root_logger

    def _configure(self):
        """
        Configures logging and structlog, and sets up exception handling.
        """
        shared_processors: list[Processor] = self._get_processors()
        self._configure_structlog(shared_processors)
        root_logger = self._configure_logging(shared_processors)
        self._clear_uvicorn_loggers()

        def handle_exception(exc_type, exc_value, exc_traceback):
            """
            Logs uncaught exceptions.
            """
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            root_logger.error(
                "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
            )

        sys.excepthook = handle_exception

    def setup_logging(self) -> BoundLogger:
        """
        Sets up logging configuration for the application.

        Returns:
            BoundLogger: The configured logger instance.
        """
        self._configure()
        return structlog.get_logger()
