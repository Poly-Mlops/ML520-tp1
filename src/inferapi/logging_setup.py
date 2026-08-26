"""Logging configuration, done once, in one place.

Configuring logging into a specific module is generally
useful to do when it is complex.
Setting up structured logging is complex, mostly boilerplate.

Note you can have the setup_logging function to have more
logic based on new parameters or the settings themselves.

The idea is to have a way of configuring it that can be maintained.
"""

import logging
import sys

from inferapi.config import LoggingConfig

# Timestamp, level and logger name are what make a line sortable, filterable, and
# traceable back to the code that wrote it. Everything else belongs in the message.
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


# NOTE(LAB): You could also use logging.dictConfig or similar
def setup_logging(log_settings: LoggingConfig) -> None:
    """Call once, at the entrypoint. `level` only throttles stdout."""
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(log_settings.level.upper())

    # TODO(LAB): add the second destination - a file handler on out/logs/app.log
    # that always captures DEBUG, whatever stdout is set to.
    # Ensure you use:
    #   log_settings.debug_file.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(stdout_handler)
    # TODO(LAB): Make sure we add the debug file if configured to do so
    ...

    # third-party libraries stay at INFO on the root
    root.setLevel(logging.INFO)
    # Ensure inferapi can receive/pass DEBUG level outputs
    #    in this setup, you have to set levels on the appropriate handlers
    #    With a single handler / basic config you can have shorter setup
    logging.getLogger("inferapi").setLevel(logging.DEBUG)
