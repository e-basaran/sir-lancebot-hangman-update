from bot.exts.fun.hangman import Hangman
# Need to export the tokens first and then run the tests
# Easier tests

def test_parse_arguments_no_args() -> None:
    """Test that calling parse_arguments with no arguments defaults to medium difficulty."""
    assert Hangman.parse_arguments(()) == ("medium", None, None)

def test_parse_arguments_help() -> None:
    """Test that 'help' argument is correctly identified."""
    assert Hangman.parse_arguments(("help",)) == (None, None, "help")

def test_parse_arguments_easy() -> None:
    """Test that 'easy' difficulty is correctly recognized."""
    assert Hangman.parse_arguments(("easy",)) == ("easy", None, None)

def test_parse_arguments_medium() -> None:
    """Test that 'medium' difficulty is correctly recognized."""
    assert Hangman.parse_arguments(("medium",)) == ("medium", None, None)

def test_parse_arguments_hard() -> None:
    """Test that 'hard' difficulty is correctly recognized."""
    assert Hangman.parse_arguments(("hard",)) == ("hard", None, None)

def test_parse_arguments_valid_custom_params() -> None:
    """Test that valid custom parameters are parsed correctly."""
    assert Hangman.parse_arguments(("5", "10")) == (None, {"min_length": 5, "max_length": 10, "min_unique_letters": 0, "max_unique_letters": 25}, None)

def test_parse_arguments_invalid_custom_params() -> None:
    """Test that invalid custom parameters return an error message."""
    assert Hangman.parse_arguments(("10", "5")) == (None, None, "Minimum word length cannot be greater than maximum word length.")

def test_parse_arguments_negative_values() -> None:
    """Test that negative custom parameters return an error message."""
    assert Hangman.parse_arguments(("-1", "5")) == (None, None, "Word length parameters cannot be negative.")

def test_parse_arguments_large_values() -> None:
    """Test that extremely large values are parsed correctly."""
    assert Hangman.parse_arguments(("5", "1000000")) == (None, {"min_length": 5, "max_length": 1000000, "min_unique_letters": 0, "max_unique_letters": 25}, None)

def test_parse_arguments_edge_case_unique_letters() -> None:
    """Test that min_unique_letters greater than max_length returns an error."""
    assert Hangman.parse_arguments(("5", "10", "11", "15")) == (None, None, "Number of unique letters cannot be greater than word length.")

def test_parse_arguments_full_custom_range() -> None:
    """Test that a full custom range is correctly parsed."""
    assert Hangman.parse_arguments(("5", "10", "2", "8")) == (None, {"min_length": 5, "max_length": 10, "min_unique_letters": 2, "max_unique_letters": 8}, None)
