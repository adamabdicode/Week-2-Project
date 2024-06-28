import requests
import json

url = 'https://opentdb.com/api.php?amount=50&category=12&difficulty=hard&type=multiple'
response = requests.get(url)

if response.status_code == 200:
    new_data = response.json()
    try:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []
    existing_data.append(new_data)
    with open("data.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
        print("Data appended to data.json file.")
else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)



# urlForFilm = 'https://opentdb.com/api.php?amount=50&category=11&difficulty=medium' #Medium Problems
# urlForFilm='https://opentdb.com/api.php?amount=50&category=11&difficulty=easy' #Easy Problems
# urlForFilm='https://opentdb.com/api.php?amount=40&category=11&difficulty=hard' #Hard Problems (40 Problems)

# urlmusic= "https://opentdb.com/api.php?amount=50&category=12&difficulty=easy"  #easy 
# urlmusic= "https://opentdb.com/api.php?amount=50&category=12&difficulty=medium"