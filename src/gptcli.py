import os
import click
import icons
from utils import program_exit
from cli_prompt import CLI_Interface
from openai_controller import check_API_key, create_new_chat_title, chat_creation
from chatlog import prepare_logs, chat_log_selector
from db import (
    init_db,
    generate_unique_ID,
    init_chat_log,
    db_message_append,
    db_update_title,
    db_get_messages,
    db_get_title,
)
from presets import presets


@click.command()
# @click.option("--temperature", "-t")
# @click.option("--help", "-h")
# @click.option("--log", "-l", default=True, help="Show Chat Logs")
@click.option("--preset", "-p", default="Q&A")
@click.option("--new_chat", "-n", default=False, help="Start a new chat")
@click.option("--api_key", "-a", help="OpenAI API keys.")
def main(api_key, new_chat=False, preset="Q&A"):
    interface = CLI_Interface(title="GPT-CLI")

    API_KEY = os.getenv("OPENAI_API_KEY") or api_key

    # Load GPT API
    if not API_KEY:
        interface.echo_prompt(
            "Failed to load API key for ChatGPT. Please check the API key."
        )
        program_exit()
    else:
        check_API_key(interface, API_KEY)

    # Choose a preset
    setting = presets[f"{preset}"]

    # Prepare GPTCLI directory and load the DB
    # Prepare chat logs
    chat_log = prepare_logs(interface)

    DB_info = init_db(chat_log)
    db = DB_info["db"]
    messages = []

    try:
        # Start a new chat
        if new_chat:
            # DB initialization using chat logs
            _id = init_chat_log(DB_info, setting, messages)
            title = db_get_title(db, _id)

            interface.echo("New chat", f"{_id}. {title}")
        # Choose a chat with ID
        else:
            # TODO
            _id = chat_log_selector(interface, db)

        title = db_get_title(db, _id)

        # Chat Begin
        count = 0
        interface = CLI_Interface(title=f"({_id}) {title}")
        while True:
            # Print previous chat
            if not new_chat and count == 0:
                messages = db_get_messages(db, _id)
                for i, msg in enumerate(messages):
                    if i % 2 == 0:
                        interface.echo_prompt(msg["content"], icon=icons.RADIO)
                    else:
                        interface.echo_user(msg["content"])

            question = interface.prompt()
            messages.append({"role": "user", "content": question})
            settings = {
                "model": setting["model"],
                "messages": messages,
            }

            # Make a title only once
            if new_chat and count == 0:
                new_title = create_new_chat_title(question)
                db_update_title(db, _id, new_title)

            interface.start_spinner("")
            response = chat_creation(settings)

            response = response.choices[0].message.content
            messages.append({"role": "system", "content": response})
            db_message_append(db, _id, messages)

            # interface.echo_user(str=response, print_option="char-by-char")
            interface.spinner_succeed(message=response, print_option="char-by-char")
            count += 1

    except Exception:
        interface.spinner_failed("Exception occurred")
        interface.echo_prompt(f"{Exception}", icon=icons.ERROR, icon_colour="red")
        interface.echo_user("")
        program_exit()
    except KeyboardInterrupt:
        interface.echo_prompt(
            "KeyboardInterrupt occurred", icon=icons.ERROR, icon_colour="red"
        )
        interface.echo_user("")
        program_exit()


if __name__ == "__main__":
    main()


# output = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": "Who won the world series in 2020?"},
#     ],
# )
# print(output)

# TODO: click (type of questions will be asked option, type of person asking option, etc)
#       figlet (letter transformation library)
