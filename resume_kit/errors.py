class ResumeKitError(Exception):
    code = "resume_kit_error"

    def __init__(self, message, detail=None):
        super().__init__(message)
        self.message = message
        self.detail = detail or {}


class MissingSourceError(ResumeKitError):
    code = "missing_source"


class OutputExistsError(ResumeKitError):
    code = "output_exists"
