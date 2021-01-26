from harc.shell import command


def status():
    statement = "systemctl status jamulus.service"
    output = command.execute(statement)
    return command.stringify(output)
