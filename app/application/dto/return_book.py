class ReturnBookResult:
    def __init__(self, success: bool, reason: str | None = None):
        self.success = success
        self.reason = reason
