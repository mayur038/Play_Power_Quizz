import requests

# Base URL
url = "https://quizapi.io/api/v1/questions"

# Query parameters
params = {
    "apiKey": "VB6YHAzJWLnTVMjQ7rtIHhKyRZlWOtIW9fC31k0p",
    "limit": 10
}

try:
    # Sending GET request
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

    # Parse JSON response
    quiz_data = response.json()

    # Print the quiz data
    print(quiz_data)

except requests.exceptions.RequestException as e:
    # Handle any errors
    print(f"Error: {e}")
