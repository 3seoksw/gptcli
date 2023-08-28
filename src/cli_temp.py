import click
import time

STEP = "◆"
STEP_DONE = "◇"
BAR = "│"
BAR_START = "┌"
BAR_END = "└"


class CLI_Interface:
    def __init__(self, title="", colour_1="green", colour_2="blue"):
        self.title = title
        self.colour_1 = colour_1
        self.colour_2 = colour_2
        self.message = ""
        self.prev_completed = False
        self.spinner = None

        DESCRIPTION = click.style(title, bg="green", fg="black")
        click.echo()
        click.echo(f"\r {BAR_START}  {DESCRIPTION}")
        click.echo(f" {BAR}")

    def replace_line(self, line_number, new_content):
        # click.echo(f"\033[{line_number};0H{new_content}\033[K")
        click.echo(f"\r{line_number}: {new_content}")

    def prompt(self, str1, str2):
        self.echo_prompt(str1)
        self.echo_user(str2)

    def echo_prompt(self, str, icon=STEP):
        if self.prev_completed:
            click.echo(f"\r {BAR}")

        styled_icon = click.style(icon, "blue")
        click.echo(f"\r {styled_icon}  {str}")

        self.prev_completed = False

    def echo_user(self, str):
        click.echo(f" {BAR}  {str}")
        click.echo(f" {BAR_END}", nl=False)
        self.prev_completed = True

    def terminate(self):
        click.echo("")


cli = CLI_Interface(title="Testing")

cli.prompt("Here's an example 1 from the program", "This is my answer")
time.sleep(1)
cli.prompt("Another Question Following up:", "Answer number 2")
time.sleep(1)
cli.prompt("Question 3!!", "My answer is 3")
cli.terminate()
