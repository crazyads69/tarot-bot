import json
import random


# Define function to read data from a json file
def read_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


# Define function to handle type of the spread and number of cards
def handle_spread(spread):
    if spread == "single":
        return 1
    elif spread == "three_card":
        return 3
    elif spread == "five_card":
        return 5
    elif spread == "celtic_cross":
        return 10
    else:
        return 1


# Define function to randomly draw a card and randomly decide if it is reversed
def draw_card(data, spread):
    random.seed(None)
    # Handle the spread
    spread = handle_spread(spread)
    # Shuffle the data
    random.shuffle(data)
    # Draw the card
    drawn_cards = []
    for i in range(spread):
        card = random.choice(data)
        reversed = random.choice([True, False])
        drawn_cards.append(
            {
                "id": card["id"],
                "predict": card["predict"],
                "meaning": card["meaning"],
                "reversed_meaning": card["reversed_meaning"],
                "name": card["name"],
                "image_path": card["image_path"],
                "suit": card["suit"],
                "reversed": reversed,
                "keywords": card["keywords"],
            }
        )
    return drawn_cards
