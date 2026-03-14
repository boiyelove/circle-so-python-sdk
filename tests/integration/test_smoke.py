"""Integration smoke tests -- run with: pytest tests/integration/ -m integration"""
import pytest
from tests.integration.conftest import requires_circle


@pytest.mark.integration
@requires_circle
class TestCommunitySmoke:
    def test_get_community(self, client):
        community = client.admin.get_community()
        assert community.id is not None
        assert community.name is not None

    def test_list_spaces(self, client):
        spaces = client.admin.spaces.list_spaces(per_page=5)
        assert spaces.page == 1
        assert isinstance(spaces.records, list)

    def test_list_members(self, client):
        members = client.admin.list_community_members(per_page=5)
        assert members.page == 1
        assert isinstance(members.records, list)
