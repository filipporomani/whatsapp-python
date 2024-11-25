from typing import Union


class Handler:
    def __init__(self, error: dict):
        self.error = error


class AuthException(Exception):  # invoked by code 0
    pass


class MethodException(AuthException):  # invoked by code 3
    pass


class ForbiddenException(AuthException):  # invoked by codes 10, 200-299
    pass


class ExpiredTokenException(AuthException):  # invoked by code 190
    pass


class ThrottlingException(Exception):  # Category exception
    pass


class RateLimitException(ThrottlingException):  # invoked by code 4
    pass


class UserRateLimitException(ThrottlingException):  # invoked by code 80007
    pass


class AppRateLimitException(ThrottlingException):  # invoked by code 130429
    pass


class SpamException(ThrottlingException):  # invoked by code 131048
    pass


class CoupleRateLimitException(ThrottlingException):  # invoked by code 131056
    pass


class RegistrationRateLimitException(ThrottlingException):  # invoked by code 133016
    pass


class IntegrityException(Exception):  # Category exception
    pass


class RulesViolationException(IntegrityException):  # invoked by code 368
    pass


class GeoRestrictionException(IntegrityException):  # invoked by code 130497
    pass


class BlockedAccountException(IntegrityException):  # invoked by code 131031
    pass


# Generic exceptions
class UnknownAPIException(Exception):  # invoked by code 1
    pass


class ServiceUnavailableException(Exception):  # invoked by code 2
    pass


class WrongPhoneNumberException(Exception):  # invoked by code 33
    pass


class InvalidParameterException(Exception):  # invoked by code 100
    pass


class ExperimentalNumberException(Exception):  # invoked by code 130472
    pass


class UnknownErrorException(Exception):  # invoked by code 131000
    pass


class AccessDeniedException(Exception):  # invoked by code 131005
    pass


class RequiredParameterMissingException(Exception):  # invoked by code 131008
    pass


class InvalidParameterTypeException(Exception):  # invoked by code 131009
    pass


class ServiceUnavailableException(Exception):  # invoked by code 131016
    pass


class SamePhoneNumberException(Exception):  # invoked by code 131021
    pass


class DeliveryFailureException(Exception):  # invoked by code 131026
    pass


class PaymentFailureException(Exception):  # invoked by code 131042
    pass


class PhoneRegistrationFailureException(Exception):  # invoked by code 131045
    pass


class ChatExpiredException(Exception):  # invoked by code 131047
    pass


class MetaDeliveryFailureException(Exception):  # invoked by code 131049
    pass


class UnsupportedMessageTypeException(Exception):  # invoked by code 131051
    pass


class MediaDownloadFailureException(Exception):  # invoked by code 131052
    pass


class MediaLoadFailureException(Exception):  # invoked by code 131053
    pass


class MaintenanceException(Exception):  # invoked by code 131057
    pass


class ParameterNumberMismatchException(Exception):  # invoked by code 132000
    pass


class ModelNotFoundException(Exception):  # invoked by code 132001
    pass


class TextTooLongException(Exception):  # invoked by code 132005
    pass


class CharacterFormatException(Exception):  # invoked by code 132007
    pass


class WrongParameterFormatException(Exception):  # invoked by code 132012
    pass


class PausedTemplateException(Exception):  # invoked by code 132015
    pass


class DisabledTemplateException(Exception):  # invoked by code 132016
    pass


class StreamBlockedException(Exception):  # invoked by code 132068
    pass


class StreamThrottlingException(Exception):  # invoked by code 132069
    pass


class FailedToRevertRegistrationException(Exception):  # invoked by code 133000
    pass


class ServerTemporaryUnavailableException(Exception):  # invoked by code 133004
    pass


class MFAPinIncorrectException(Exception):  # invoked by code 133005
    pass


class PhoneVerificationRequiredException(Exception):  # invoked by code 133006
    pass


class TooManyPinAttemptsException(Exception):  # invoked by code 133008
    pass


class TooFastPinAttemptsException(Exception):  # invoked by code 133009
    pass


class UnregisteredNumberException(Exception):  # invoked by code 133010
    pass


class RetryLaterException(Exception):  # invoked by code 133015
    pass


class GenericUserException(Exception):  # invoked by code 135000
    pass


pairings = {
    0: AuthException,
    1: UnknownAPIException,
    2: ServiceUnavailableException,
    3: MethodException,
    4: RateLimitException,
    10: ForbiddenException,
    33: WrongPhoneNumberException,
    100: InvalidParameterException,
    200: ForbiddenException,
    130429: AppRateLimitException,
    130472: ExperimentalNumberException,
    130497: GeoRestrictionException,
    131000: UnknownErrorException,
    131005: AccessDeniedException,
    131008: RequiredParameterMissingException,
    131009: InvalidParameterTypeException,
    131016: ServiceUnavailableException,
    131021: SamePhoneNumberException,
    131026: DeliveryFailureException,
    131042: PaymentFailureException,
    131045: PhoneRegistrationFailureException,
    131047: ChatExpiredException,
    131048: SpamException,
    131049: MetaDeliveryFailureException,
    131051: UnsupportedMessageTypeException,
    131052: MediaDownloadFailureException,
    131053: MediaLoadFailureException,
    131056: CoupleRateLimitException,
    131057: MaintenanceException,
    132000: ParameterNumberMismatchException,
    132001: ModelNotFoundException,
    132005: TextTooLongException,
    132007: CharacterFormatException,
    132012: WrongParameterFormatException,
    132015: PausedTemplateException,
    132016: DisabledTemplateException,
    132068: StreamBlockedException,
    132069: StreamThrottlingException,
    133000: FailedToRevertRegistrationException,
    133004: ServerTemporaryUnavailableException,
    133005: MFAPinIncorrectException,
    133006: PhoneVerificationRequiredException,
    133008: TooManyPinAttemptsException,
    133009: TooFastPinAttemptsException,
    133010: UnregisteredNumberException,
    133015: RetryLaterException,
    80007: UserRateLimitException,
    131031: BlockedAccountException,
    131056: CoupleRateLimitException,
    131057: MaintenanceException,
    133016: RegistrationRateLimitException,
    368: RulesViolationException,
    190: ExpiredTokenException,
}


class Handle:
    def __init__(self, data: dict) -> Union[Exception, None]:
        try:
            code = data["error"]["code"]
            if code in pairings:
                raise pairings[code]({"error": data["error"]["message"], "code": code})
            else: 
                if code in range(200, 300):
                    raise ForbiddenException({"error": data["error"]["message"], "code": code})
            raise Handler(Exception({"error": data["error"]["message"], "code": code}))
        except KeyError:
            return None