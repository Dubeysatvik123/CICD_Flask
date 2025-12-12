import pytest
from unittest.mock import patch, MagicMock
from project1 import evaluate_startup_idea

# Test empty prompt
def test_evaluate_startup_idea_with_empty_prompt():
    result = evaluate_startup_idea("")
    assert result == "Please enter your startup idea to get an evaluation."

# Test successful evaluation with mocked model
@patch("project1.genai.GenerativeModel")  # patch the model class itself
def test_evaluate_startup_idea_success(mock_model_class):
    # Create a mock object to simulate the conversation
    mock_convo = MagicMock()
    mock_convo.send_message.return_value.text = "Sample evaluation response."

    # Make the mocked GenerativeModel instance return the mock conversation
    mock_instance = MagicMock()
    mock_instance.start_chat.return_value = mock_convo
    mock_model_class.return_value = mock_instance

    prompt = "An AI tool that matches pet owners with ideal pets based on their habits."
    result = evaluate_startup_idea(prompt)

    # Assert that the evaluation response contains the mocked text
    assert "Sample evaluation response." in result

# Optional: Additional test for error handling or other edge cases
@patch("project1.genai.GenerativeModel")
def test_evaluate_startup_idea_model_failure(mock_model_class):
    # Simulate a model that raises an exception
    mock_instance = MagicMock()
    mock_instance.start_chat.side_effect = Exception("Model failure")
    mock_model_class.return_value = mock_instance

    prompt = "Some startup idea"
    result = evaluate_startup_idea(prompt)

    assert "Error" in result or "Please enter" not in result  # adjust based on your function's error handling
