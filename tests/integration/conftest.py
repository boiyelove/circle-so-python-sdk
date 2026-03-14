"""Integration test fixtures -- skip if env vars not set."""
import os
import pytest
from circle import CircleClient

CIRCLE_API_TOKEN = os.environ.get("CIRCLE_API_TOKEN")
CIRCLE_COMMUNITY_URL = os.environ.get("CIRCLE_COMMUNITY_URL")

requires_circle = pytest.mark.skipif(
    not CIRCLE_API_TOKEN, reason="CIRCLE_API_TOKEN env var not set"
)


@pytest.fixture(scope="session")
def client():
    if not CIRCLE_API_TOKEN:
        pytest.skip("CIRCLE_API_TOKEN not set")
    url = CIRCLE_COMMUNITY_URL or "https://app.circle.so"
    c = CircleClient(api_token=CIRCLE_API_TOKEN, community_url=url)
    yield c
    c.close()
