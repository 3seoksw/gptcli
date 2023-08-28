import time
import threading
import sys
import click
import icons
from utils import program_exit


UNICODE_SUPPORT = sys.stdout.encoding in (
    "UTF-8",
    "UTF-16",
    "UTF-16LE",
    "UTF-16BE",
    "UTF-32",
    "UTF-32LE",
    "UTF32BE",
)

CHECK = icons.CHECK
X = icons.X
DELAY = 0.08
if UNICODE_SUPPORT:
    SPINNER_FRAMES = icons.SPINNER_FRAMES
else:
    SPINNER_FRAMES = icons.SPINNER_FRAMES_2


class Spinner:
    def __init__(
        self,
        message="",
        active=False,
        spinner_frames=SPINNER_FRAMES,
        delay=DELAY,
        spinner_colour="green",
        text_colour="black",
        output_format=click,
    ):
        self.message = message
        self.active = active
        self.is_succeed = False
        self.spinner_frames = spinner_frames
        self.delay = delay
        self.spinner_colour = spinner_colour
        self.text_colour = text_colour
        self.frame_index = 0
        self.spinner_stop = None
        self.output_format = output_format
        self.flag = False

    def print_spinner(self, cli_interface):
        while self.active:
            for frame in self.spinner_frames:
                cli_interface.echo_prompt(
                    "\r " + click.style(frame, fg="yellow") + f" {self.message}",
                    nl_flag=self.flag,
                )
                time.sleep(self.delay)

    def _spin(self, cli_interface):
        self.print_spinner(cli_interface)

        return self

    def start(self, cli_interface, message="Loading"):
        if self.active:
            return

        self.message = message

        self.active = True
        self.spinner_thread = threading.Thread(target=self._spin, args=(cli_interface,))
        self.spinner_thread.start()

    def succeed(self, cli_interface, message, print_option):
        self.is_succeed = True
        self.stop()
        if print_option == "default":
            cli_interface.echo_prompt(
                "\r " + click.style(CHECK, fg="green") + f"  {message}", self.flag
            )
            cli_interface.echo_user("")
        elif print_option == "char-by-char":
            cli_interface.echo_user(
                str="\r " + click.style(CHECK, fg="green") + f"  {message}",
                print_option=print_option,
            )

    def failed(self, cli_interface, message):
        self.is_succeed = False
        self.stop()
        cli_interface.echo_prompt("\r " + click.style(X, fg="red") + f"  {message}")
        cli_interface.echo_user("")
        program_exit()

    def stop(self):
        self.active = False
        if self.spinner_thread:
            self.spinner_thread.join()
            self.spinner_thread = None


# Testing Code
# sp = Spinner()
# sp.start("Loading for testing")
# time.sleep(3)
# sp.succeed("Test Completed")
