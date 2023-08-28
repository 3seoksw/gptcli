import os
import click
import icons
from db import db_get_all_chats, db_get_db_by_id
from utils import program_exit

BAR = icons.BAR = "│"
CHECKBOX_DEACTIVATE = icons.CHECKBOX_DEACTIVATE


home_dir = os.path.expanduser("~")
folder_name = "gptcli/"
gptcli_dir = os.path.join(home_dir, folder_name)
log_file = "chat_log.json"
chat_log_dir = os.path.join(gptcli_dir, log_file)

GPTCLI = click.style("gptcli", fg="green")
coloured_filename = click.style(f"{log_file}", fg="cyan")


def prepare_logs(interface):
    if not os.path.exists(gptcli_dir):
        interface.echo_prompt(
            icon=icons.ERROR,
            icon_colour="yellow",
            str=f"No directory for {GPTCLI} found",
        )
        interface.echo_indent()

        os.mkdir(gptcli_dir)
        interface.echo_prompt(
            str=f"New {GPTCLI} directory created!",
            icon=icons.CHECK,
            icon_colour="green",
        )

    if not os.path.exists(chat_log_dir):
        with open(chat_log_dir, "x") as f:
            f.write("")
            interface.echo_indent()
            interface.echo_prompt(
                str=f"New file created: {coloured_filename}",
                icon=icons.CHECK,
                icon_colour="green",
            )
            interface.echo_nl()

    return chat_log_dir


def chat_log_selector(interface, db):
    chats = db_get_all_chats(db)

    if len(chats) == 0:
        interface.terminate("No chat logs found")
        program_exit()
    else:
        styled_log_dir = click.style(chat_log_dir, fg="cyan")
        selected_id = interface.echo_selector(
            f"Choose a chat with ID (loaded from {styled_log_dir:}):", chats
        )
        selected_id = int(selected_id)

        return selected_id
        # return db_get_db_by_id(db, selected_id)

    # TODO: add keyboard listener to add interactivity
    # sel = click.Choice(list, case_sensitive=True)
    # click.prompt("Select", type=sel, show_choices=True, show_default=False)
