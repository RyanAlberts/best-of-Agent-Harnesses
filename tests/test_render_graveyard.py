import generate
def test_readme_has_graveyard_section_and_excludes_from_main():
    md = generate.generate_readme()
    assert "## ⚰️ Graveyard" in md
    gid = next(g for g in generate.ARCHIVED if generate.is_graveyard(g))
    body, _, grave = md.partition("## ⚰️ Graveyard")
    assert gid in grave and gid not in body  # archived repo only under Graveyard
