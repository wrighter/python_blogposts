import datetime

import testbook

@testbook.testbook('./jupyter_unit_tests.ipynb', execute=True)
def test_make_url(tb):
    f = tb.ref("make_url")
    d = "2020-01-02"
    assert f(d) == "https://api.example.com/v2/2020/1/2"

    # note that this is actually converted to a string
    d = datetime.date(2020,1,2)
    assert f(d) == "https://api.example.com/v2/2020/1/2"

    # this one will be testing the date functionality
    d2 = tb.ref("testdate1")
    assert f(d2) == "https://api.example.com/v2/2020/1/1"

    # this one will inject similar code as above, then use it
    tb.inject("d3 = datetime.date(2020, 2, 3)")
    d3 = tb.ref("d3")
    assert f(d3) == "https://api.example.com/v2/2020/2/3"


