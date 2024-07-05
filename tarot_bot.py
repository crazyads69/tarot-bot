from sympy import sec
from draw_card import draw_card, read_json_file
import os
import dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from prompt import SINGLE_CARD_PROMPT, THREE_CARD_PROMPT


# Define the main function
def main():
    # Load env
    dotenv.load_dotenv()

    # Set the API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
        generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
            max_output_tokens=8192,
            temperature=0.8,
            top_p=1.0,
        ),
    )
    # Read the processed data
    data = read_json_file(r"./processed_data.json")
    # Draw a single card
    drawn_card = draw_card(data, "three_card")
    user_question = "Liệu tôi không thể trở thành người yêu với crush cũ của mình?"
    # create the formatted drawn card
    first_card = f"""
    **Tên lá bài Tarot:** {drawn_card[0]["name"] if not drawn_card[0]["reversed"] else f"{drawn_card[0]['name']} (đảo ngược)"}
    **Ý nghĩa:** {drawn_card[0]["meaning"] if not drawn_card[0]["reversed"] else drawn_card[0]["reversed_meaning"]}
    **Mục đích:** {drawn_card[0]["predict"]}
    **Keyword:** {drawn_card[0]["keywords"]}
    """
    second_card = f"""
    **Tên lá bài Tarot:** {drawn_card[1]["name"] if not drawn_card[1]["reversed"] else f"{drawn_card[1]['name']} (đảo ngược)"}
    **Ý nghĩa:** {drawn_card[1]["meaning"] if not drawn_card[1]["reversed"] else drawn_card[1]["reversed_meaning"]}
    **Mục đích:** {drawn_card[1]["predict"]}
    **Keyword:** {drawn_card[1]["keywords"]}
    """
    third_card = f"""
    **Tên lá bài Tarot:** {drawn_card[2]["name"] if not drawn_card[2]["reversed"] else f"{drawn_card[2]['name']} (đảo ngược)"}
    **Ý nghĩa:** {drawn_card[2]["meaning"] if not drawn_card[2]["reversed"] else drawn_card[2]["reversed_meaning"]}
    **Mục đích:** {drawn_card[2]["predict"]}
    **Keyword:** {drawn_card[2]["keywords"]}
    """
    # Create the prompt
    # prompt = f"{SINGLE_CARD_PROMPT.format(user_question=user_question, drawn_card=drawn_card)}"
    prompt = f"{THREE_CARD_PROMPT.format(user_question=user_question, first_card=first_card, second_card=second_card, third_card=third_card)}"
    # Generate the response
    try:
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return


if __name__ == "__main__":
    main()
