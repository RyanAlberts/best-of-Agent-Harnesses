import json

import write_queue


def test_write_fills_defaults_and_normalizes(tmp_path):
    out = tmp_path / "curation-queue.json"
    sample_data = {
        "generated": "2026-07-03",
        "movers": [{"id": "foo/bar", "from": 100, "to": 150}],
    }

    result = write_queue.write(sample_data, out)

    loaded = json.loads(out.read_text())

    for key in ("generated", "movers", "moved", "archived", "failed", "candidates"):
        assert key in loaded
        assert key in result

    generated = loaded["generated"]
    assert len(generated) == 10 and generated[4] == "-" and generated[7] == "-"

    assert loaded["movers"] == [{"id": "foo/bar", "from": 100, "to": 150}]
    assert loaded["moved"] == []
    assert loaded["archived"] == []
    assert loaded["failed"] == []
    assert loaded["candidates"] == []

    assert result == loaded


def test_write_defaults_when_all_keys_omitted(tmp_path):
    out = tmp_path / "curation-queue.json"

    result = write_queue.write({}, out)

    loaded = json.loads(out.read_text())
    assert loaded["movers"] == []
    assert loaded["moved"] == []
    assert loaded["archived"] == []
    assert loaded["failed"] == []
    assert loaded["candidates"] == []
    assert "generated" in loaded
    assert result == loaded
