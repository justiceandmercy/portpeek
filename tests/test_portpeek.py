import json

from portpeek import parse

SAMPLE = """COMMAND     PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3   1234  alice  3u  IPv4  0x0  0t0  TCP *:8000 (LISTEN)
node      5678  bob    4u  IPv6  0x0  0t0  TCP [::]:3000 (LISTEN)
nginx     9999  root   6u  IPv4  0x0  0t0  TCP 127.0.0.1:80 (LISTEN)
"""


def test_parse_count():
    assert len(parse(SAMPLE)) == 3


def test_parse_ports():
    rows = parse(SAMPLE)
    assert {r["port"] for r in rows} == {8000, 3000, 80}


def test_parse_fields():
    row = next(r for r in parse(SAMPLE) if r["port"] == 3000)
    assert row["command"] == "node"
    assert row["pid"] == 5678
    assert row["user"] == "bob"


def test_parse_empty():
    assert parse("COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n") == []


def test_json_serializable():
    assert json.loads(__import__("json").dumps(parse(SAMPLE)))
