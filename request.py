import argparse
import requests

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Send a POST or GET request to a URL with a message')

    # Add the URL argument
    parser.add_argument('--url', type=str, help='the URL to send the request to', default='http://localhost:8080/facade_service')

    # Add the request type argument
    parser.add_argument('--request_type', type=str, choices=['post', 'get'], help='the type of request to send', default='post')

    # Add the message argument
    parser.add_argument('--msg', type=str, help='the message to include in the request', default='hello')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the URL, request type, and message from the parsed arguments
    url = args.url
    request_type = args.request_type
    message = args.msg

    # Make the request based on the request type
    if request_type == 'post':
        # Define the JSON data to be sent in the request
        json_data = {
            'msg': message
        }
        
        # Make the POST request with the JSON data
        response = requests.post(url, json=json_data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Access the response data
            data = response.json()
            print(data)
        else:
            print('Error:', response.status_code)

    elif request_type == 'get':

        
        # Make the GET request with the query parameters
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Access the response data
            data = response.json()
            print(data)
        else:
            print('Error:', response.status_code)

if __name__ == "__main__":
    main()