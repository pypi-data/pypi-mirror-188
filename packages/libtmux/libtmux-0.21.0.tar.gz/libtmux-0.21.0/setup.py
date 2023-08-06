# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['libtmux', 'libtmux._internal', 'libtmux._vendor']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['libtmux = libtmux.pytest_plugin']}

setup_kwargs = {
    'name': 'libtmux',
    'version': '0.21.0',
    'description': 'Typed scripting library / ORM / API wrapper for tmux',
    'long_description': '# libtmux\n\nlibtmux is a [typed](https://docs.python.org/3/library/typing.html) python scripting library for tmux. You can use it to command and control tmux servers,\nsessions, windows, and panes. It is the tool powering [tmuxp], a tmux workspace manager.\n\n[![Python Package](https://img.shields.io/pypi/v/libtmux.svg)](https://pypi.org/project/libtmux/)\n[![Docs](https://github.com/tmux-python/libtmux/workflows/docs/badge.svg)](https://libtmux.git-pull.com/)\n[![Build Status](https://github.com/tmux-python/libtmux/workflows/tests/badge.svg)](https://github.com/tmux-python/tmux-python/actions?query=workflow%3A%22tests%22)\n[![Code Coverage](https://codecov.io/gh/tmux-python/libtmux/branch/master/graph/badge.svg)](https://codecov.io/gh/tmux-python/libtmux)\n[![License](https://img.shields.io/github/license/tmux-python/libtmux.svg)](https://github.com/tmux-python/libtmux/blob/master/LICENSE)\n\nlibtmux builds upon tmux\'s\n[target](http://man.openbsd.org/OpenBSD-5.9/man1/tmux.1#COMMANDS) and\n[formats](http://man.openbsd.org/OpenBSD-5.9/man1/tmux.1#FORMATS) to\ncreate an object mapping to traverse, inspect and interact with live\ntmux sessions.\n\nView the [documentation](https://libtmux.git-pull.com/),\n[API](https://libtmux.git-pull.com/api.html) information and\n[architectural details](https://libtmux.git-pull.com/about.html).\n\n# Install\n\n```console\n$ pip install --user libtmux\n```\n\n# Open a tmux session\n\nSession name `foo`, window name `bar`\n\n```console\n$ tmux new-session -s foo -n bar\n```\n\n# Pilot your tmux session via python\n\n```console\n$ python\n```\n\nUse [ptpython], [ipython], etc. for a nice shell with autocompletions:\n\n```console\n$ pip install --user ptpython\n```\n\n```console\n$ ptpython\n```\n\nConnect to a live tmux session:\n\n```python\n>>> import libtmux\n>>> s = libtmux.Server()\n>>> s\nServer(socket_path=/tmp/tmux-.../default)\n```\n\nTip: You can also use [tmuxp]\'s [`tmuxp shell`] to drop straight into your\ncurrent tmux server / session / window pane.\n\n[tmuxp]: https://tmuxp.git-pull.com/\n[`tmuxp shell`]: https://tmuxp.git-pull.com/cli/shell.html\n[ptpython]: https://github.com/prompt-toolkit/ptpython\n[ipython]: https://ipython.org/\n\nList sessions:\n\n```python\n>>> server.sessions\n[Session($1 ...), Session($0 ...)]\n```\n\nFilter sessions by attribute:\n\n```python\n>>> server.sessions.filter(history_limit=\'2000\')\n[Session($1 ...), Session($0 ...)]\n```\n\nDirect lookup:\n\n```python\n>>> server.sessions.get(session_id="$1")\nSession($1 ...)\n```\n\nFind session by dict lookup:\n\n```python\n>>> server.sessions[0].rename_session(\'foo\')\nSession($1 foo)\n>>> server.sessions.filter(session_name="foo")[0]\nSession($1 foo)\n```\n\nControl your session:\n\n```python\n>>> session.rename_session(\'foo\')\nSession($1 foo)\n>>> session.new_window(attach=False, window_name="ha in the bg")\nWindow(@2 2:ha in the bg, Session($1 foo))\n>>> session.kill_window("ha in")\n```\n\nCreate new window in the background (don\'t switch to it):\n\n```python\n>>> session.new_window(attach=False, window_name="ha in the bg")\nWindow(@2 2:ha in the bg, Session($1 ...))\n```\n\nClose window:\n\n```python\n>>> w = session.attached_window\n>>> w.kill_window()\n```\n\nGrab remaining tmux window:\n\n```python\n>>> window = session.attached_window\n>>> window.split_window(attach=False)\nPane(%2 Window(@1 1:... Session($1 ...)))\n```\n\nRename window:\n\n```python\n>>> window.rename_window(\'libtmuxower\')\nWindow(@1 1:libtmuxower, Session($1 ...))\n```\n\nSplit window (create a new pane):\n\n```python\n>>> pane = window.split_window()\n>>> pane = window.split_window(attach=False)\n>>> pane.select_pane()\nPane(%3 Window(@1 1:..., Session($1 ...)))\n>>> window = session.new_window(attach=False, window_name="test")\n>>> window\nWindow(@2 2:test, Session($1 ...))\n>>> pane = window.split_window(attach=False)\n>>> pane\nPane(%5 Window(@2 2:test, Session($1 ...)))\n```\n\nType inside the pane (send key strokes):\n\n```python\n>>> pane.send_keys(\'echo hey send now\')\n\n>>> pane.send_keys(\'echo hey\', enter=False)\n>>> pane.enter()\nPane(%1 ...)\n```\n\nGrab the output of pane:\n\n```python\n>>> pane.clear()  # clear the pane\nPane(%1 ...)\n>>> pane.send_keys("cowsay \'hello\'", enter=True)\n>>> print(\'\\n\'.join(pane.cmd(\'capture-pane\', \'-p\').stdout))  # doctest: +SKIP\n$ cowsay \'hello\'\n _______\n< hello >\n -------\n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||\n...\n```\n\nTraverse and navigate:\n\n```python\n>>> pane.window\nWindow(@1 1:..., Session($1 ...))\n>>> pane.window.session\nSession($1 ...)\n```\n\n# Python support\n\nUnsupported / no security releases or bug fixes:\n\n- Python 2.x: The backports branch is\n  [`v0.8.x`](https://github.com/tmux-python/libtmux/tree/v0.8.x).\n\n# Donations\n\nYour donations fund development of new features, testing and support.\nYour money will go directly to maintenance and development of the\nproject. If you are an individual, feel free to give whatever feels\nright for the value you get out of the project.\n\nSee donation options at <https://git-pull.com/support.html>.\n\n# Project details\n\n- tmux support: 1.8+\n- python support: >= 3.7, pypy, pypy3\n- Source: <https://github.com/tmux-python/libtmux>\n- Docs: <https://libtmux.git-pull.com>\n- API: <https://libtmux.git-pull.com/api.html>\n- Changelog: <https://libtmux.git-pull.com/history.html>\n- Issues: <https://github.com/tmux-python/libtmux/issues>\n- Test Coverage: <https://codecov.io/gh/tmux-python/libtmux>\n- pypi: <https://pypi.python.org/pypi/libtmux>\n- Open Hub: <https://www.openhub.net/p/libtmux-python>\n- Repology: <https://repology.org/project/python:libtmux/versions>\n- License: [MIT](http://opensource.org/licenses/MIT).\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/tmux-python/libtmux/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
