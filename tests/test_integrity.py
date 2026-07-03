import generate
import check_integrity


def test_verify_passes_on_real_data():
    violations = check_integrity.verify()
    assert violations == []


def test_verify_flags_empty_category():
    cat_id = generate.CATEGORIES[0][0]
    original = generate.PROJECTS[cat_id]
    generate.PROJECTS[cat_id] = []
    try:
        violations = check_integrity.verify()
    finally:
        generate.PROJECTS[cat_id] = original
    assert any(cat_id in v for v in violations)


def _stub_repo(tmp_path, intro_text):
    (tmp_path / "README.md").write_text(intro_text + "\n")
    (tmp_path / "comparisons").mkdir()
    for name in ["how-to-pick-a-harness.md", "memory-layers.md",
                 "multi-agent-orchestration.md", "openclaw-vs-hermes.md",
                 "terminal-coding-agents.md"]:
        (tmp_path / "comparisons" / name).write_text("# Heading\n" + ("x" * 3000))
    return tmp_path


def test_verify_flags_missing_intro_sentinel(tmp_path, monkeypatch):
    _stub_repo(tmp_path, "# Nothing interesting here")
    monkeypatch.setattr(check_integrity, "REPO_ROOT", tmp_path)
    violations = check_integrity.verify()
    assert any("README" in v or "intro" in v.lower() for v in violations)


def test_verify_flags_thin_comparison_file(tmp_path, monkeypatch):
    _stub_repo(tmp_path, check_integrity.INTRO_SENTINEL)
    (tmp_path / "comparisons" / "memory-layers.md").write_text("# H\ntoo short")
    monkeypatch.setattr(check_integrity, "REPO_ROOT", tmp_path)
    violations = check_integrity.verify()
    assert any("memory-layers.md" in v for v in violations)


def test_verify_flags_mass_data_loss(monkeypatch):
    def fake_run_git_show():
        return {"project_count": 10000, "graveyard_count": 0}

    monkeypatch.setattr(check_integrity, "_previous_totals", fake_run_git_show)
    violations = check_integrity.verify()
    assert any("data loss" in v.lower() or "dropped" in v.lower() for v in violations)


def test_main_exits_nonzero_on_violation(monkeypatch, capsys):
    monkeypatch.setattr(check_integrity, "verify", lambda: ["fake violation"])
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        check_integrity.main()
    assert exc_info.value.code == 1
    out = capsys.readouterr().out
    assert "fake violation" in out


def test_main_exits_zero_when_clean(monkeypatch, capsys):
    monkeypatch.setattr(check_integrity, "verify", lambda: [])
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        check_integrity.main()
    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "integrity OK" in out
