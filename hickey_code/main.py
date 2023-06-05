'''
Demo code for interacting with GPT-3 in Python.
This code comes from an article on medium.com
https://medium.com/codingthesmartway-com-blog/how-to-use-chatgpt-with-python-1213b8477f7b

To run this you need to 
* first visit openai.com and get an APIkey, which you insert into the code below.
  get the apikey at this URL https://platform.openai.com/account/api-keys
* next create a folder and put this file in the folder as gptapi.py
* finally run the following commands

% pip3 install openai  (on Mac, or pip install openai on Windows/Linux)
% python3 gptapi.py  (on Mac, or python gptapi.py on Windows/Linux)
'''
import openai

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"

messages = ["You are a realestate AI here to help customers. You are an expert on realesate in Boston and you know the best deals on Zillow, Craiglist etc... ."]

while True:
    prompt = input("Enter a prompt: ") # "Hello, how are you today?"

    messages.append(prompt)

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    print(response)

    if prompt == "exit":
        break
