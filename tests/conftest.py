import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Sample activities data for testing."""
    return {
        "Test Club": {
            "description": "A test club for testing purposes",
            "schedule": "Test schedule",
            "max_participants": 5,
            "participants": ["test1@mergington.edu", "test2@mergington.edu"]
        },
        "Empty Club": {
            "description": "An empty test club",
            "schedule": "Test schedule",
            "max_participants": 10,
            "participants": []
        }
    }


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test."""
    from src.app import activities
    original_activities = activities.copy()
    yield
    activities.clear()
    activities.update(original_activities)