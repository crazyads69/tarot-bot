import json

from sympy import im


# Read the json file and generate the data to feed to the LLM
def read_json_file(file_path):
    with open(file_path, "r") as f:
        # Load the data from the json file encoded in utf-8
        data = json.load(f)
    return data["tarot_interpretations"]


def handle_suit(data):
    # Handle suit to return the correct image path
    suit = data["suit"]
    if suit == "major":
        return "major"
    elif suit == "wands":
        return "wands"
    elif suit == "cups":
        return "cups"
    elif suit == "swords":
        return "swords"
    elif suit == "coins":
        return "pents"


# Process the data to generate the training data for the LLM
def process_data(data):
    index = 1
    process_data = []
    for entry in data:
        # First create the index
        id = index
        predict = entry["fortune_telling"]
        meaning = entry["meanings"]["light"]
        reversed_meaning = entry["meanings"]["shadow"]
        name = entry["name"]
        # Check if the name contain words "coins" and replace it with "pentacles"
        if "coins" in name:
            name = name.replace("coins", "pentacles")
        # Capitalize the first letter of each word in the name
        name = " ".join([word.capitalize() for word in name.split()])
        # Check the suit of the card
        suit = handle_suit(entry)
        keywords = entry["keywords"]
        # Generate the image path
        rank = entry["rank"]
        if rank == "page" and suit != "major":
            image_path = f"./img/{suit}11.jpg"
        elif rank == "knight" and suit != "major":
            image_path = f"./img/{suit}12.jpg"
        elif rank == "queen" and suit != "major":
            image_path = f"./img/{suit}13.jpg"
        elif rank == "king" and suit != "major":
            image_path = f"./img/{suit}14.jpg"
        elif suit == "major":
            # create image index
            custom_rank = entry["rank"]
            image_index = 0
            if custom_rank < 10:
                image_index = f"0{rank}"
            else:
                image_index = rank
            image_path = f"./img/maj{image_index}.jpg"
        else:
            # create image index
            custom_rank = entry["rank"]
            image_index = 0
            if custom_rank < 10:
                image_index = f"0{custom_rank}"
            else:
                image_index = custom_rank
            image_path = f"./img/{suit}{image_index}.jpg"
        # Append the data to the process_data list
        process_data.append(
            {
                "id": id,
                "predict": predict,
                "meaning": meaning,
                "reversed_meaning": reversed_meaning,
                "name": name,
                "keywords": keywords,
                "image_path": image_path,
                "suit": suit,
            }
        )
        index += 1
    # Return the processed data
    return process_data


if __name__ == "__main__":
    # Read the json file
    data = read_json_file(r"./tarot_data.json")

    # Process the data
    processed_data = process_data(data)

    # Write the processed data to a json file
    with open("processed_data.json", "w") as f:
        json.dump(processed_data, f, indent=4)

    print("Data has been processed and saved to processed_data.json")
