import pytest

from barbuilder import Menu


def test_render():
    m = Menu()
    m.title = 'title'
    m.add_item('option 1')
    m.add_header('title2', length=20)
    i = m.add_item('option 2', color='green')
    i.add_item('suboption1', sfimage='calendar')
    i.add_divider()
    s = i.add_item('suboption2')
    s.href = 'https://github.com/swiftbar/SwiftBar'
    i.set_alternate('alt')
    i.add_item('suboption3', shell='/some/command', param0='"this is text"; rm -rf /')
    out = str(m)
    assert out == """\
title
title2 | length=20
---
option 1
option 2 | color=green
--suboption1 | sfimage=calendar
-----
--suboption2 | href=https://github.com/swiftbar/SwiftBar
--suboption3 | shell=/some/command param0='"this is text"; rm -rf /'
alt | alternate=True
"""
