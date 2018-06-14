import logging


def init_logger():
    log = logging.getLogger('gopac')
    log.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter(
        '#%(levelname)-s, %(name)s, %(pathname)s, line %(lineno)d: %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setFormatter(console_formatter)

    log.addHandler(console_handler)

    return log
