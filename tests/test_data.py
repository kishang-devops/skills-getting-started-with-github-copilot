import pytest
from src.app import activities


class TestDataValidation:
    """Test class for data validation and structure."""
    
    def test_activities_data_structure(self):
        """Test that activities data has the correct structure."""
        assert isinstance(activities, dict)
        assert len(activities) > 0
        
        for activity_name, activity_data in activities.items():
            # Check required fields exist
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            
            # Check data types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            
            # Check constraints
            assert activity_data["max_participants"] > 0
            assert len(activity_data["participants"]) <= activity_data["max_participants"]
            
            # Check participant emails
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation

    def test_default_activities_exist(self):
        """Test that expected default activities exist."""
        expected_activities = [
            "Chess Club",
            "Programming Class", 
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Workshop",
            "Drama Club",
            "Mathletes",
            "Science Club"
        ]
        
        for activity in expected_activities:
            assert activity in activities, f"Expected activity '{activity}' not found"

    def test_participant_email_format(self):
        """Test that all participant emails follow expected format."""
        for activity_name, activity_data in activities.items():
            for email in activity_data["participants"]:
                assert "@mergington.edu" in email, f"Invalid email format: {email}"

    def test_activity_names_not_empty(self):
        """Test that activity names are not empty."""
        for activity_name in activities.keys():
            assert activity_name.strip() != ""
            assert len(activity_name) > 0

    def test_descriptions_not_empty(self):
        """Test that activity descriptions are not empty."""
        for activity_data in activities.values():
            assert activity_data["description"].strip() != ""
            assert len(activity_data["description"]) > 10  # Reasonable description length