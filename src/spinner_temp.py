import time
import threading
import sys
import click


UNICODE_SUPPORT = sys.stdout.encoding in (
    "UTF-8",
    "UTF-16",
    "UTF-16LE",
    "UTF-16BE",
    "UTF-32",
    "UTF-32LE",
    "UTF32BE",
)

CHECK = "✓"
X = "x"
DELAY = 0.08
if UNICODE_SUPPORT:
    SPINNER_FRAMES = ["◒", "◐", "◓", "◑"]
else:
    SPINNER_FRAMES = ["•", "o", "O", "0"]


class Spinner:
    def __init__(
        self,
        message="",
        active=False,
        spinner_frames=SPINNER_FRAMES,
        delay=DELAY,
        spinner_colour="green",
        text_colour="black",
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

    def print_spinner(self):
        while self.active:
            for frame in self.spinner_frames:
                click.echo(
                    "\r" + click.style(frame, fg="yellow") + f" {self.message}",
                    nl=False,
                )
                time.sleep(self.delay)

    def _spin(self):
        self.print_spinner()

        return self

    def start(self, message="Loading"):
        if self.active:
            return

        self.message = message

        self.active = True
        self.spinner_thread = threading.Thread(
            target=self._spin,
        )
        self.spinner_thread.start()

    def succeed(self, message):
        self.is_succeed = True
        self.stop()
        click.echo("\r" + click.style(CHECK, fg="green") + f" {message}")

    def failed(self, message):
        self.is_succeed = False
        self.stop()
        click.echo("\r" + click.style(X, fg="red") + f" {message}")

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
