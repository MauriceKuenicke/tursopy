class MissingRequiredAttributeException(Exception):
    """Indicate a missing required attribute."""


class TokenAlreadyExistsException(Exception):
    """Indicate an already existing token during creation."""


class TokenNotFoundException(Exception):
    """Indicate a missing token."""


class InvalidPlatformTokenException(Exception):
    """Indicate an invalid platform token"""


class NotFoundExceptions(Exception):
    """Indicates a not found error."""


class TursoRequestException(Exception):
    """Indicates an error during a request."""
