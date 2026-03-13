"""
Unit tests for text_cleaner and pdf_extractor services.
"""

from app.services.text_cleaner import clean_text


def test_clean_text_ligatures():
    assert clean_text("\ufb01gure") == "figure"
    assert clean_text("\ufb02ow") == "flow"
    assert clean_text("\ufb00ect") == "ffect"


def test_clean_text_merged_words():
    assert clean_text("wordWord") == "word Word"
    assert clean_text("someThingHere") == "some Thing Here"


def test_clean_text_missing_space_after_period():
    assert clean_text("end.Start") == "end. Start"
    assert clean_text("stop.Next") == "stop. Next"


def test_clean_text_missing_space_after_comma():
    assert clean_text("one,two,three") == "one, two, three"


def test_clean_text_multiple_spaces():
    assert clean_text("too  many   spaces") == "too many spaces"


def test_clean_text_no_change_needed():
    text = "This is already clean text."
    assert clean_text(text) == text
