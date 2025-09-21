import requests

def test_translation():
    # URL of your translation service
    url = 'http://127.0.0.1:5000/translate'
    
    # Test data
    data = {
        'text': 'hello',
        'target_language': 'es'
    }
    
    # Send POST request
    response = requests.post(url, json=data)
    
    # Print the response
    print('Status Code:', response.status_code)
    print('Response:', response.json())

if __name__ == '__main__':
    test_translation()
