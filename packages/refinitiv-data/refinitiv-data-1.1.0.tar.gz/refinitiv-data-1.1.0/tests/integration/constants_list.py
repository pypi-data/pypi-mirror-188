class HttpStatusCode(object):
    TWO_HUNDRED = 200
    FOUR_HUNDRED = 400
    FOUR_HUNDRED_THREE = 403
    FOUR_HUNDRED_FOUR = 404
    FOUR_HUNDRED_TWELVE = 412


class HttpReason(object):
    OK = "OK"
    BAD_REQUEST = "Bad Request"
    NOT_FOUND = "Not Found"


class Intervals(object):
    ONE_MINUTE = "PT1M"
    FIVE_MINUTES = "PT5M"
    TEN_MINUTES = "PT10M"
    THIRTY_MINUTES = "PT30M"
    SIXTY_MINUTES = "PT60M"
    ONE_HOUR = "PT1H"
    DAILY = "P1D"
    SEVEN_DAYS = "P7D"
    WEEKLY = "P1W"
    MONTHLY = "P1M"
    QUARTERLY = "P3M"
    TWELVE_MONTHS = "P12M"
    YEARLY = "P1Y"


ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
