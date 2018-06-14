class DownloadCancel(Exception):
    pass


class GoPacException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CliNotFound(GoPacException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ErrorDecodeOutput(GoPacException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DownloadPacFileException(GoPacException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SavePacFileException(GoPacException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
