class CliNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ErrorDecodeOutput(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GoPacException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
