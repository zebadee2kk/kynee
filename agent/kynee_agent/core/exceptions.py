"""KYNEĒ core exceptions."""


class KyneeException(Exception):
    """Base exception for all KYNEĒ errors."""

    pass


class PolicyViolationError(KyneeException):
    """Raised when a policy constraint is violated."""

    pass


class OutOfScopeError(PolicyViolationError):
    """Raised when target is outside engagement scope."""

    pass


class RateLimitExceededError(PolicyViolationError):
    """Raised when rate limit is exceeded."""

    pass


class UnauthorizedMethodError(PolicyViolationError):
    """Raised when a method is not authorized."""

    pass


class TimeWindowViolationError(PolicyViolationError):
    """Raised when action is outside authorized time window."""

    pass


class EngagementError(KyneeException):
    """Raised when engagement has issues."""

    pass


class InvalidRoEError(EngagementError):
    """Raised when Rules of Engagement are invalid."""

    pass


class AuditLogError(KyneeException):
    """Raised when audit log operations fail."""

    pass


class ConfigurationError(KyneeException):
    """Raised when configuration is invalid."""

    pass


class TransportError(KyneeException):
    """Raised when transport layer fails."""

    pass


class EnrollmentError(TransportError):
    """Raised when device enrollment fails."""

    pass
