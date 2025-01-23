import logging


__all__ = ("create_logger",)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger
