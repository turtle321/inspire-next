from requests.models import Response

from . import exceptions


class BaseOrcidClientResponse(dict):
    exceptions = (exceptions.TokenInvalidException,)

    def __init__(self, memberapi, response):
        if isinstance(response, dict):
            data = response
            self.raw_response = memberapi.raw_response
        elif isinstance(response, Response):
            data = response.json()
            self.raw_response = response
        else:
            raise ValueError('response must be a dict or a requests\' Response')
        super(BaseOrcidClientResponse, self).__init__(data)

    @property
    def ok(self):
        return self.raw_response.ok

    @property
    def status_code(self):
        return self.raw_response.status_code

    def raise_for_result(self):
        """
        Check the "result" of the call. The "result" is determined not
        only by the HTTP status code, but it might also take into
        consideration the actual content of the response.
        It might raise one of the known exceptions (in self.exceptions)
        depending on the matching criteria; or it might raise
        requests.exceptions.HTTPError.
        In case of no errors no exception is raised.
        """
        for exception_class in self.exceptions:
            if exception_class.match(self):
                exception_object = exception_class(str(self))
                exception_object.raw_response = self.raw_response
                raise exception_object
        # Can raise requests.exceptions.HTTPError.
        return self.raw_response.raise_for_status()
