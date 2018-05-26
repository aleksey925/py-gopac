class CliNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ErrorDecodeOutput(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class GoPacException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
