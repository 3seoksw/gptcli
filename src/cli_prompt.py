import click
import time
import icons
from spinner import Spinner

STEP = icons.STEP = "◆"
STEP_DONE = icons.STEP_DONE = "◇"
RADIO = icons.RADIO
CHECKBOX_DEACTIVATE = icons.CHECKBOX_DEACTIVATE
CHECKBOX_ACTIVATE = icons.CHECKBOX_ACTIVATE
BAR = icons.BAR = "│"
BAR_START = icons.BAR_START = "┌"
BAR_END = icons.BAR_END = "└"
BAR_CONNECT = icons.BAR_CONNECT = "├"
BAR_H = icons.BAR_H = "─"


class CLI_Interface:
    def __init__(self, title="", icon_colour="blue", text_colour="black"):
        self.title = title
        self.icon_colour = icon_colour
        self.text_colour = text_colour
        self.message = ""
        self.prev_completed = False
        self.indented = False
        self.spinner = Spinner()

        DESCRIPTION = click.style(title, bg="green", fg="black")
        click.echo()
        click.echo(f"\r {BAR_START}  {DESCRIPTION}")
        click.echo(f" {BAR}")

    def replace_line(self, line_number, new_content):
        # click.echo(f"\033[{line_number};0H{new_content}\033[K")
        click.echo(f"\r{line_number}: {new_content}")

    def echo(
        self,
        str1,
        str2,
        icon=STEP,
        icon_colour="blue",
        text_colour="black",
        nl_flag=True,
    ):
        self.echo_prompt(str1, icon, icon_colour, text_colour, nl_flag)
        self.echo_user(str2)

    def echo_prompt(
        self,
        str,
        icon=STEP,
        icon_colour="blue",
        text_colour="black",
        nl_flag=True,
    ):
        if self.prev_completed:
            click.echo(f"\r {BAR}")

        styled_icon = click.style(icon, icon_colour)
        if not self.indented:
            click.echo(f"\r {styled_icon}  {str}", nl=nl_flag)
        else:
            click.echo(f" {styled_icon}  {str}", nl=nl_flag)
            self.indented = False

        self.prev_completed = False

    def echo_user(self, str, print_option="default"):
        if print_option == "default":
            click.echo(f" {BAR}  {str}")
            click.echo(f" {BAR_END}", nl=False)
        elif print_option == "char-by-char":
            click.echo(f" {BAR}  ", nl=False)
            for char in str:
                if char == "\n":
                    click.echo("")
                    click.echo(f" {BAR}  ", nl=False)
                else:
                    click.echo(char, nl=False)
                time.sleep(0.01)
            click.echo("")
            click.echo(f" {BAR_END}", nl=False)
        self.prev_completed = True

    def echo_nl(self):
        click.echo(f" {BAR}")

    def echo_indent(self):
        click.echo(f" {BAR}")
        click.echo(f" {BAR_CONNECT}{BAR_H}", nl=False)
        self.indented = True

    def echo_selector(self, str, list):
        self.echo_prompt(str)

        deactivated = click.style(f"{CHECKBOX_DEACTIVATE}", fg="cyan")
        for i in range(len(list)):
            click.echo(f" {BAR}  {deactivated}  {list[i]['_id']}. {list[i]['title']}")

        click.echo(f" {BAR_END}", nl=False)

        selection = self.prompt(icon=icons.ARROW, icon_colour="cyan")

        self.prev_completed = True

        return selection

    def prompt(self, icon=RADIO, icon_colour="blue"):
        if self.prev_completed:
            click.echo(f"\r {BAR}")

        radio_icon = click.style(f" {icon} ", fg=icon_colour)
        self.prev_completed = False
        return click.prompt("\r", prompt_suffix=radio_icon)

    def terminate(self, text=""):
        click.echo(text)

    def start_spinner(self, message):
        self.spinner.start(self, message)

    def spinner_succeed(self, message, print_option="default"):
        self.spinner.succeed(self, message=message, print_option=print_option)

    def spinner_failed(self, message):
        self.spinner.failed(self, message)

    def spinner_stop(self):
        self.spinner.stop()


# Test Code
# cli = CLI_Interface(title="Testing")

# cli.prompt("Here's an example 1 from the program", "This is my answer")
# time.sleep(1)
# cli.prompt("Another Question Following up:", "Answer number 2")
# time.sleep(1)
# cli.prompt("Question 3!!", "My answer is 3")
# time.sleep(1)

# cli.start_spinner("Test Loading")
# time.sleep(3)
# cli.spinner_succeed("Test Success!")

# cli.start_spinner("Testing 2")
# time.sleep(3)
# cli.spinner_failed("Test 2 Failed!")

# cli.terminate()
