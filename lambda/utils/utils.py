_ERRORS = {
    100: "Unspecified Error",
    101: "Could not render speech",
    102: "Could not render display",
    103: "Could not render APL",
    104: "Could not load APL Document JSON",
    105: "Could not customize APL Document JSON",
    106: "Could not render APL Directive",
}


def store_command(handler_input, cmd):
    """
    Store a command to be sent with the next connection.
    """
    handler_input.attributes_manager.session_attributes["COMMAND"] = cmd
