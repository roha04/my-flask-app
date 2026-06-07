class ServiceError(Exception):
    """Base service-layer error."""


class NotFoundError(ServiceError):
    pass


class ConflictError(ServiceError):
    pass


class UnauthorizedError(ServiceError):
    pass


class ValidationError(ServiceError):
    pass
