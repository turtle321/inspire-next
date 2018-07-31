import pytest

from inspirehep.modules.orcid.service.client import OrcidClient

from utils import override_config


CONFIG = dict(
    # ORCID_SANDBOX=False,
    # SERVER_NAME='https://labs.inspirehep.net',
    # ORCID_APP_CREDENTIALS={
    #     'consumer_secret': 'dc3db0a3-59eb-4132-ace8-98508ba0c155',
    #     'consumer_key': '0000-0001-8607-8906'
    # },
)


@pytest.mark.usefixtures('isolated_app')
class TestGetAllWorksSummary(object):
    def setup_class(self):
        """Run only once before the first test method."""
        self.config = dict(
            ORCID_SANDBOX=False,
            ORCID_APP_CREDENTIALS={
                'consumer_secret': 'dc3db0a3-59eb-4132-ace8-98508ba0c155',  # TODO cambia!!!!!
                'consumer_key': '0000-0001-8607-8906'  # TODO cambia!!!!
            },
        )

    def setup(self):
        """Run before each test method."""
        oauth_token = '1b85185e-30c0-4f62-aae2-e04d5846a04a'   # TODO cambia!!!!!
        orcid = '0000-0002-0942-3697'
        self.client = OrcidClient(oauth_token, orcid)

    def test_happy_flow(self):
        with override_config(**self.config):
            response = self.client.get_all_works_summary()
        response.raise_for_result()
        assert response.ok


FALLISCEEEEEE ^^^^^