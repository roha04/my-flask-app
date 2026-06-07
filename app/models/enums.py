import enum


class ApplicationStage(str, enum.Enum):
    WISHLIST = "Wishlist"
    APPLIED = "Applied"
    PHONE_SCREEN = "PhoneScreen"
    TECHNICAL = "Technical"
    ONSITE = "Onsite"
    OFFER = "Offer"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class JobStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class NoteEntityType(str, enum.Enum):
    COMPANY = "company"
    JOB = "job"
    APPLICATION = "application"
