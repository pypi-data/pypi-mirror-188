# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygsc']

package_data = \
{'': ['*']}

install_requires = \
['blessed', 'click', 'pygame', 'pyparsing', 'urwid']

entry_points = \
{'console_scripts': ['gsc = pygsc.cli:gsc',
                     'gsc-display-keycodes = pygsc.cli:display_keycodes',
                     'gsc-monitor = pygsc.cli:gsc_monitor',
                     'gsc-monitor-test-client = '
                     'pygsc.cli:gsc_monitor_test_client',
                     'gsc-monitor-test-server = '
                     'pygsc.cli:gsc_monitor_test_server',
                     'gsc-record = pygsc.cli:gsc_record']}

setup_kwargs = {
    'name': 'pygsc',
    'version': '0.6',
    'description': 'Run command-line demos from a script.',
    'long_description': '# Description\n\n`pygsc` is a Python script that lets you run shell scripts *interactively*. This is useful for doing live command line demos.\n\n![Basic Demo](./demo/gsc-basic-demo.gif)\n\n`pygsc` is a (another) rewrite of [`gsc`](https://github.com/CD3/gsc). There is a long history with the creation of this tool for a computer class I teach. You can read it\nthere.\n\n## Features\n\n- Run shell scripts "interactively".\n    - Characters are sent to the shell, on at a time, each time you press a key.\n    - When the end of a line has been reached, press enter to go to the next line.\n- Script *any* command line application: vim, gnuplot, ssh, etc.\n- Modal : switch between insert mode, command mode, and pass through mode (see below).\n    - If you run into an error in your script (a typo, or some file that is missing), you can switch to pass-through mode to quickly fix the error without\n      exiting the demo.\n- Statusline in the upper right corner of the terminal lets you know where you are and what mode your in. This can be disabled.\n- Reload scripts while running without starting over. If you reload a script, its contents are updated, but the position in the demo is maintained.\n\n## Installing\n\nTo install, clone this repository and run pip in the root directory.\n\n```\n$ git clone <URL_FOR_THIS_REPO>\n$ cd pygsc\n$ pip install .\n```\n\nOr can also install the latest release from PyPi.\n```\n$ pip install pygsc\n```\n\nNote these may not be up-to-date with the latest changes in the repository.\n\n## Usage\n\nTo start a demo, run `gsc` with the script\n\n```bash\n$ gsc my_demo.sh\n```\n\nThis will start shell (by default, `$SHELL`) in a forked process and connect to it with a psuedo terminal. Each line in the script\nis then loaded and sent to the shell, on character at a time, while the user types. Once the entire line has been sent, `gsc` waits\nfor the user to press return, and the next line is loaded.\n\nYou can specify a different shell with the `--shell` option.\n\n```bash\n$ gsc my_demo.sh --shell zsh\n```\n\n\n\n### Keybindings\n\n#### Insert Mode\n\nInsert mode is the main mode, `gsc` starts up in insert mode. While in insert mode, `gsc` will read each line of the script and send\ncharacters to the shell each time the user presses a key. When an entire line has been sent to the shell, `gsc` will wait for the user\nto press enter before starting the next line in the script.\n\n`<any character>`: send next character to shell.\n\n`return`: if at the end of current script line send `\\r` and load next script line. otherwise, send next character.\n\n`ctrl-d`: switch to command mode.\n\n`ctrl-p`: switch to pass-through mode.\n\n`ctrl-c`: exit `gsc`\n\n#### Line Mode\n\nLine mode is special type of insert mode where entire lines are sent to the shell instead of single characters. This mode is useful for\nquickly testing a script.\n\n`<any character>`: send next line to the shell.\n\n`return`: send `\\r` to shell and load next script line.\n\n`ctrl-d`: switch to command mode.\n\n`ctrl-c`: exit `gsc`\n\n#### Command Mode\n\nCommand mode allows the user to make (simple) adjustments during the demo. The user can move the current character position, for example\nto skip a line or backup.\n\n`i`: switch to insert mode.\n\n`I`: switch to line mode.\n\n`p`: switch to pass-through mode.\n\n`j`: jump to the next line in the script.\n\n`k`: jump to the previous line in the script.\n\n`h`: jump to the previous character in the current script line.\n\n`k`: jump to the next character in the current script line.\n\n`^`: jump to the first character in the current script line.\n\n`$`: jump to the end of the current script line (one past the last character).\n\n`s`: toggle status line on/off.\n\n`R`: reload scripts (useful for developing scripts, you can edit the script in a text file while running and reload).\n\n#### Pass-through Mode\n\nPass-through mode sends all user input to the shell. This can be used to fix the current line, fix the environment (remove files that are not supposed to be there),\nor just temporarily take over the demo.\n\n`ctrl-d`: switch to command mode.\n\n`ctrl-p`: switch to insert mode (`ctrl-p` acts as a toggle between insert and pass-through mode).\n\n#### Temporary Pass-through Mode\n\nTemporary Pass-through mode is a special version of pass-through mode that exits as soon as the user pressed return. It is useful for allowing the user to insert a password.\n\n`return`: send `\\r` to shell and switch back to previous mode.\n\n\n\n### Commands\n\nA script may embed commands in its comments. These are special keywords recognized by `gsc` that will cause\nsome side effect or action to take place. Commands may provide arguments that will be processed by `gsc` when\nthe command is recognized. The syntax for a command is\n\n```\n# name[:  [arg1 [arg2 [...]]]]\n```\n\nIf a command takes arguments, a colon \':\' must separate the command name from the arguments. Multiple arguments\nare separated by spaces. If an argument contains spaces, it must be quoted.\n\n`pause: N`\n\nPause the session for `N` seconds. If `N` is less than zero, the session will be paused until the user presses a key.\n\n`display: \'message to display\'`\n\nDisplay a message in a separate display window. This command requires a message display backend to be installed.\nCurrently, the only backend supported is `pygame`. So, to use this command, `pygame` must be installed.\n\n`passthrough`\n\nSwitch to pass-through mode. See above.\n\n`temporary passthrough`\n\nSwitch to temporary pass-through mode. See above.\n\n`line`\n\nSwitch to line mode. See above.\n\n`statusline: [on|off]`\n\nEnable/disable the status line.\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
