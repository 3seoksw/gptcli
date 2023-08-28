import click


def program_exit():
    click.echo(click.style("  Exiting ", fg="red"), nl=False)
    click.echo(click.style("gptcli", fg="green", bold=True), nl=False)
    click.echo(click.style("...", fg="red"))
    exit()
