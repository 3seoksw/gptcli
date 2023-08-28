import openai
from utils import program_exit


def check_API_key(interface, api_key):
    try:
        interface.start_spinner("Verifying API key")

        openai.api_key = api_key
        openai.Model.list()

        interface.spinner_succeed(f"API key valid: {api_key}")
    except openai.OpenAIError:
        interface.spinner_failed(f"Invalid API key: {api_key}")

        program_exit()


def chat_creation(settings):
    response = openai.ChatCompletion.create(
        model=settings["model"],  # string:
        messages=settings["messages"],  # list: [{"role": "user", "content": "~"}]
        # temperature=settings.temperature
    )

    return response


def create_new_chat_title(input):
    messages = [
        {
            "role": "system",
            "content": "You're job is to create a new chat title based on the context of the user's input. The title you will be generating will be at most length of 5 words.",
        }
    ]
    messages.append({"role": "user", "content": input})

    settings = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }

    response = chat_creation(settings)

    return response["choices"][0]["message"]["content"]
