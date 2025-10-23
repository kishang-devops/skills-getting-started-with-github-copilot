import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestActivitiesAPI:
    """Test class for activities API endpoints."""
    
    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index.html."""
        response = client.get("/")
        assert response.status_code == 200
        # Should redirect or serve the static file

    def test_get_activities(self, client):
        """Test getting all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Should contain the default activities
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_structure(self, client):
        """Test the structure of activities data."""
        response = client.get("/activities")
        data = response.json()
        
        # Check structure of first activity
        first_activity = list(data.values())[0]
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in first_activity
        
        assert isinstance(first_activity["participants"], list)
        assert isinstance(first_activity["max_participants"], int)

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity."""
        response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for non-existent activity."""
        response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_participant(self, client):
        """Test that duplicate signup is prevented."""
        email = "duplicate@mergington.edu"
        activity = "Chess Club"
        
        # First signup should succeed
        response1 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Second signup should fail
        response2 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]

    def test_signup_updates_participants_list(self, client):
        """Test that signup actually adds participant to the list."""
        email = "newparticipant@mergington.edu"
        activity = "Chess Club"
        
        # Get initial participants
        response = client.get("/activities")
        initial_participants = response.json()[activity]["participants"]
        initial_count = len(initial_participants)
        
        # Sign up
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Check participants updated
        response = client.get("/activities")
        updated_participants = response.json()[activity]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert email in updated_participants

    def test_unregister_from_activity_success(self, client):
        """Test successful unregistration from an activity."""
        # First, sign up a user
        email = "test@mergington.edu"
        activity = "Chess Club"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Then unregister
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregistration from non-existent activity."""
        response = client.delete("/activities/Nonexistent Club/unregister?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_non_participant(self, client):
        """Test unregistration of non-participant."""
        response = client.delete("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_removes_participant(self, client):
        """Test that unregistration actually removes participant from the list."""
        email = "toremove@mergington.edu"
        activity = "Chess Club"
        
        # Sign up first
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Verify they're in the list
        response = client.get("/activities")
        participants_before = response.json()[activity]["participants"]
        assert email in participants_before
        
        # Unregister
        client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Verify they're removed
        response = client.get("/activities")
        participants_after = response.json()[activity]["participants"]
        assert email not in participants_after
        assert len(participants_after) == len(participants_before) - 1

    def test_activity_capacity_tracking(self, client):
        """Test that activity capacity is properly tracked."""
        response = client.get("/activities")
        activities_data = response.json()
        
        for name, details in activities_data.items():
            participants_count = len(details["participants"])
            max_participants = details["max_participants"]
            assert participants_count <= max_participants
            
    def test_email_parameter_handling(self, client):
        """Test various email parameter formats."""
        activity = "Chess Club"
        
        # Test with URL encoded email
        response = client.post(f"/activities/{activity}/signup?email=user%40mergington.edu")
        assert response.status_code == 200
        
        # Test with plus sign in email
        response = client.post(f"/activities/{activity}/signup?email=user+test@mergington.edu")
        assert response.status_code == 200

    def test_activity_name_with_spaces(self, client):
        """Test activities with spaces in names."""
        # "Chess Club" has spaces, test it works
        response = client.post("/activities/Chess Club/signup?email=spacetest@mergington.edu")
        assert response.status_code == 200
        
        # Test URL encoded activity name
        response = client.post("/activities/Chess%20Club/signup?email=spacetest2@mergington.edu")
        assert response.status_code == 200