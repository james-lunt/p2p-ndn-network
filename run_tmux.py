
import os
import shlex
import shutil
import sys

import libtmux


def run_in_tmux():
    """Run a command in a new tmux window."""
    #script_name = os.path.basename(sys.argv[0])

    # Tmux session
    tmux_server = libtmux.Server()
    try:
        tmux_sessions = tmux_server.list_sessions()
    # pylint: disable=broad-except
    except Exception:
        tmux_sessions = None


    session = tmux_sessions[1]

    #  Execute the command
    command_str = "python node.py --name /divers/diver1"
    command_str2 = "python node.py --name /divers/diver1/light"

    #session.new_window(attach=True, window_shell=command_str)
    window = session.new_window(attach=True, window_name="heu")
    window1 = session.new_window(attach=True, window_name="heu2")
    #pane = window.split_window()
    #print(pane.select_pane())
    window.send_keys(command_str)
    #pane1 = window1.split_window()
    #pane1.send_keys(command_str2)



if __name__ == '__main__':
    run_in_tmux()