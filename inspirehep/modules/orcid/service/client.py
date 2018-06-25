from flask import current_app
from orcid import MemberAPI

from time_execution import time_execution


class OrcidService(object):
    def __init__(self, oauth_token, orcid):
        self.oauth_token = oauth_token
        self.orcid = orcid
        client_key = current_app.config['ORCID_APP_CREDENTIALS']['consumer_key']
        client_secret = current_app.config['ORCID_APP_CREDENTIALS']['consumer_secret']
        sandbox = current_app.config['ORCID_SANDBOX']
        self.memberapi = MemberAPI(client_key, client_secret, sandbox, timeout=30)

    @time_execution
    def put_updated_work(self, xml_data, putcode):
        response = self.memberapi.update_record(
            orcid_id=self.orcid,
            token=self.oauth_token,
            request_type='work',
            data=xml_data,
            put_code=putcode,
            content_type='application/orcid+xml',
        )
        return PutUpdatedWorkResponse(self.memberapi, response)

    @time_execution
    def post_new_work(self, xml_data):
        response = self.memberapi.add_record(
            orcid_id=self.orcid,
            token=self.oauth_token,
            request_type='work',
            data=xml_data,
            content_type='application/orcid+xml',
        )
        return PostNewWorkResponse(self.memberapi, response)

    @time_execution
    def get_all_works(self):
        response = self.memberapi.read_record_member(
            self.orcid,
            'works',
            self.oauth_token,
            accept_type='application/orcid+json',
        )
        """
        Response is a dict like:
{'group': [{'external-ids': {'external-id': [{'external-id-relationship': 'SELF',
                                              'external-id-type': 'doi',
                                              'external-id-url': {'value': 'http://dx.doi.org/10.1016/0029-5582(61)90469-2'},
                                              'external-id-value': '10.1016/0029-5582(61)90469-2'}]},
            'last-modified-date': {'value': 1519143190177},
            'work-summary': [{'created-date': {'value': 1516716146242},
                              'display-index': '0',
                              'external-ids': {'external-id': [{'external-id-relationship': 'SELF',
                                                                'external-id-type': 'doi',
                                                                'external-id-url': {'value': 'http://dx.doi.org/10.1016/0029-5582(61)90469-2'},
                                                                'external-id-value': '10.1016/0029-5582(61)90469-2'}]},
                              'last-modified-date': {'value': 1519143190177},
                              'path': '/0000-0002-1825-0097/work/912978',
                              'publication-date': {'day': None,
                                                   'media-type': None,
                                                   'month': None,
                                                   'year': {'value': '1961'}},
                              'put-code': 912978,
                              'source': {'source-client-id': {'host': 'sandbox.orcid.org',
                                                              'path': 'CHANGE_ME',
                                                              'uri': 'http://sandbox.orcid.org/client/CHANGE_ME'},
                                         'source-name': {'value': 'INSPIRE-PROFILE-PUSH'},
                                         'source-orcid': None},
                              'title': {'subtitle': None,
                                        'title': {'value': 'Partial Symmetries of Weak Interactions'},
                                        'translated-title': None},
                              'type': 'JOURNAL_ARTICLE',
                              'visibility': 'PUBLIC'}]}],
 'last-modified-date': {'value': 1519143233490},
 'path': '/0000-0002-1825-0097/works'}
        """
        return GetAllWorksResponse(self.memberapi, response)

    @time_execution
    def get_works(self, putcode):
        response = self.memberapi.read_record_member(
            self.orcid,
            'works',
            self.oauth_token,
            accept_type='application/orcid+json',
            put_code=putcode,
        )
        """
        Response is a dict like:
{'bulk': [{'work': {'citation': {'citation-type': 'BIBTEX',
                                 'citation-value': u''},
                    'contributors': {'contributor': [{'contributor-attributes': {'contributor-role': 'AUTHOR',
                                                                                 'contributor-sequence': 'FIRST'},
                                                      'contributor-email': None,
                                                      'contributor-orcid': None,
                                                      'credit-name': {'value': 'Glashow, S.L.'}}]},
                    'country': None,
                    'created-date': {'value': 1516716146242},
                    'external-ids': {'external-id': [{'external-id-relationship': 'SELF',
                                                      'external-id-type': 'doi',
                                                      'external-id-url': {'value': 'http://dx.doi.org/10.1016/0029-5582(61)90469-2'},
                                                      'external-id-value': '10.1016/0029-5582(61)90469-2'}]},
                    'journal-title': {'value': 'Nucl.Phys.'},
                    'language-code': None,
                    'last-modified-date': {'value': 1519143190177},
                    'path': None,
                    'publication-date': {'day': None,
                                         'media-type': None,
                                         'month': None,
                                         'year': {'value': '1961'}},
                    'put-code': 912978,
                    'short-description': None,
                    'source': {'source-client-id': {'host': 'sandbox.orcid.org',
                                                    'path': 'CHANGE_ME',
                                                    'uri': 'http://sandbox.orcid.org/client/CHANGE_ME'},
                               'source-name': {'value': 'INSPIRE-PROFILE-PUSH'},
                               'source-orcid': None},
                    'title': {'subtitle': None,
                              'title': {'value': 'Partial Symmetries of Weak Interactions'},
                              'translated-title': None},
                    'type': 'JOURNAL_ARTICLE',
                    'url': {'value': 'http://labs.inspirehep.net/record/4328'},
                    'visibility': 'PUBLIC'}}]}        
        """
        return GetWorksResponse(self.memberapi, response)


class OrcidServiceResponse(object):
    def __init__(self, memberapi):
        self.raw_response = memberapi.response
        self.http_status_code = memberapi.response.status_code


class PutUpdatedWorkResponse(OrcidServiceResponse):
    pass


class PostNewWorkResponse(OrcidServiceResponse):
    def __init__(self, memberapi, response):
        super(PostNewWorkResponse, self).__init__(memberapi)
        self.putcode = response


class GetAllWorksResponse(OrcidServiceResponse):
    def __init__(self, memberapi, response):
        super(GetAllWorksResponse, self).__init__(memberapi)
        self.works = response


class GetWorksResponse(OrcidServiceResponse):
    def __init__(self, memberapi, response):
        super(GetWorksResponse, self).__init__(memberapi)
        self.work = response



# TODO find a way to define exceptions
# TODO shall reponses be dict objects or data models?