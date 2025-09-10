"""Unit test for business logic (completion_rate)."""
from app.business_layer.book import summarize_book_title

def test_summarize_book_title_basic():
    assert summarize_book_title("The Great Gatsby") == "the-great-gatsby"
    assert summarize_book_title("One") == "one"
    assert summarize_book_title("") == "untitled"
    assert summarize_book_title("  Leading and Trailing  Spaces ") == "leading-and-trailing"
