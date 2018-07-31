import mock

from inspirehep.modules.orcid.service import exceptions


class MyExcpetion(exceptions.BaseOrcidClientJsonException):
    http_status_code = 401
    content = {
        'error': 'invalid_token'
    }


def test_match_positive():
    response = mock.MagicMock()
    response.status_code = 401
    response.get.return_value = 'invalid_token'
    assert MyExcpetion.match(response)


def test_match_negative_content():
    response = mock.MagicMock()
    response.status_code = 401
    response.get.return_value = 'xxx'
    assert not MyExcpetion.match(response)


def test_match_negative_status_code():
    response = mock.MagicMock()
    response.status_code = 400
    response.get.return_value = 'invalid_token'
    assert not MyExcpetion.match(response)
