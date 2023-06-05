import os
import openai
from colorama import Fore, Back, Style

# configure OpenAI
openai.api_key = "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"

INSTRUCTIONS = """Welcome to our real estate bot! Our purpose is to provide you with a seamless real estate experience. Here's how we can assist you: 

Firstly, we can help you search for properties based on your specific requirements, such as location, size, price range, and amenities. Our bot will provide you with real-time listings and personalized recommendations. 

Secondly, we offer detailed information about properties, including descriptions, images, floor plans, virtual tours, and neighborhood data. Feel free to ask us any specific questions about a property, and we'll provide you with the relevant details you need. 

If you're curious about the market value of a property, our bot can estimate it using algorithms and data analysis. This will give you a rough idea of its worth, helping you make informed decisions. 

For those looking for financing options, we can guide you through the mortgage process. Our bot will explain different loan types, calculate monthly payments, and clarify eligibility criteria. 

Scheduling property viewings and appointments is hassle-free with our bot. We sync with real estate agents' calendars to suggest available time slots and send reminders to both parties. 

If you're torn between multiple properties, our bot can assist you in comparing them side by side. It will highlight key features, pros, and cons, allowing you to make a more informed decision. 

Staying up to date with real estate market trends is essential, and our bot provides you with the latest information on prices, supply and demand, and neighborhood developments. 

Lastly, we can offer general guidance on real estate laws, regulations, and documentation requirements, ensuring you have a basic understanding of the legal aspects involved. 

With our real estate bot, we aim to simplify and streamline your real estate journey, saving you time and effort in your property search, decision-making, and transaction processes.
"""

TEMPERATURE = 0.1
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorif    ies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "What can I get you?: " + Style.RESET_ALL
        )

        if new_question == "exit":
            break

        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, you're question didn't pass the moderation check:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue

        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Here you go: " + Style.NORMAL + response)

    print(previous_questions_and_answers)



if __name__ == "__main__":
    main()