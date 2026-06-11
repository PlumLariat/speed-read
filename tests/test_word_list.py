import pytest

from core.word_list import WordList


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def wl():
    return WordList()


@pytest.fixture
def txt_file(tmp_path):
    def _make(content: str) -> str:
        f = tmp_path / "test.txt"
        f.write_text(content, encoding="utf-8")
        return str(f)
    return _make


@pytest.fixture
def three_word_list(txt_file):
    wl = WordList()
    wl.init_from_txt_file(txt_file("one two three"))
    return wl


@pytest.fixture
def single_word_list(txt_file):
    wl = WordList()
    wl.init_from_txt_file(txt_file("only"))
    return wl


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

class TestInit:
    def test_list_is_empty(self, wl):
        assert wl.l == []

    def test_cur_index_is_zero(self, wl):
        assert wl.cur_index == 0

    def test_remaining_is_zero(self, wl):
        assert wl.remaining == 0

    def test_not_complete(self, wl):
        assert wl.complete is False


# ---------------------------------------------------------------------------
# init_from_txt_file
# ---------------------------------------------------------------------------

class TestInitFromTxtFile:
    def test_loads_words(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("one two three"))
        assert wl.l == ["one", "two", "three"]

    def test_remaining_is_len_minus_one(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("one two three"))
        assert wl.remaining == 2

    def test_cur_index_unchanged(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("one two three"))
        assert wl.cur_index == 0

    def test_single_word_remaining_is_zero(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("only"))
        assert wl.remaining == 0

    def test_single_word_list(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("only"))
        assert wl.l == ["only"]

    def test_splits_on_newlines(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("one\ntwo\nthree"))
        assert wl.l == ["one", "two", "three"]

    def test_splits_on_tabs(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("one\ttwo\tthree"))
        assert wl.l == ["one", "two", "three"]

    def test_ignores_extra_whitespace(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("  one   two  \n  three  "))
        assert wl.l == ["one", "two", "three"]

    def test_unicode_content(self, wl, txt_file):
        wl.init_from_txt_file(txt_file("café naïve résumé"))
        assert wl.l == ["café", "naïve", "résumé"]

    def test_reload_replaces_existing_words(self, three_word_list, txt_file):
        three_word_list.init_from_txt_file(txt_file("new words"))
        assert three_word_list.l == ["new", "words"]
        assert three_word_list.remaining == 1

    def test_file_not_found_raises(self, wl):
        with pytest.raises(FileNotFoundError):
            wl.init_from_txt_file("nonexistent_file.txt")


# ---------------------------------------------------------------------------
# get_current_word
# ---------------------------------------------------------------------------

class TestGetCurrentWord:
    def test_returns_first_word_initially(self, three_word_list):
        assert three_word_list.get_current_word() == "one"

    def test_returns_correct_word_after_advance(self, three_word_list):
        three_word_list.next()
        assert three_word_list.get_current_word() == "two"

    def test_returns_last_word_at_end(self, three_word_list):
        three_word_list.next()
        three_word_list.next()
        assert three_word_list.get_current_word() == "three"

    def test_raises_on_empty_list(self, wl):
        with pytest.raises(IndexError):
            wl.get_current_word()


# ---------------------------------------------------------------------------
# next
# ---------------------------------------------------------------------------

class TestNext:
    def test_advances_cur_index(self, three_word_list):
        three_word_list.next()
        assert three_word_list.cur_index == 1

    def test_decrements_remaining(self, three_word_list):
        three_word_list.next()
        assert three_word_list.remaining == 1

    def test_advances_through_all_words(self, three_word_list):
        words = [three_word_list.get_current_word()]
        three_word_list.next()
        words.append(three_word_list.get_current_word())
        three_word_list.next()
        words.append(three_word_list.get_current_word())
        assert words == ["one", "two", "three"]

    def test_sets_complete_when_last_word_reached(self, three_word_list):
        three_word_list.next()
        three_word_list.next()
        assert three_word_list.complete is False
        three_word_list.next()
        assert three_word_list.complete is True

    def test_does_not_advance_past_last_word(self, three_word_list):
        three_word_list.next()
        three_word_list.next()
        three_word_list.next()
        assert three_word_list.cur_index == 2

    def test_complete_persists_after_repeated_calls(self, three_word_list):
        for _ in range(10):
            three_word_list.next()
        assert three_word_list.complete is True
        assert three_word_list.cur_index == 2

    def test_single_word_sets_complete_on_first_call(self, single_word_list):
        single_word_list.next()
        assert single_word_list.complete is True

    def test_single_word_cur_index_stays_zero(self, single_word_list):
        single_word_list.next()
        assert single_word_list.cur_index == 0

    def test_not_complete_before_last_next(self, three_word_list):
        three_word_list.next()
        three_word_list.next()
        assert three_word_list.complete is False


# ---------------------------------------------------------------------------
# prev
# ---------------------------------------------------------------------------

class TestPrev:
    def test_prev_does_not_move_back(self, three_word_list):
        # Guard `if self.remaining >= 0: return` means prev() never executes
        # its body under normal conditions since remaining is always >= 0.
        three_word_list.next()
        three_word_list.prev()
        assert three_word_list.cur_index == 1

    def test_prev_does_not_change_remaining(self, three_word_list):
        three_word_list.next()
        before = three_word_list.remaining
        three_word_list.prev()
        assert three_word_list.remaining == before

    def test_prev_at_start_does_nothing(self, three_word_list):
        three_word_list.prev()
        assert three_word_list.cur_index == 0
        assert three_word_list.remaining == 2


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------

class TestReset:
    def test_resets_cur_index_to_zero(self, three_word_list):
        three_word_list.next()
        three_word_list.reset()
        assert three_word_list.cur_index == 0

    def test_resets_remaining(self, three_word_list):
        three_word_list.next()
        three_word_list.reset()
        assert three_word_list.remaining == 2

    def test_clears_complete_flag(self, three_word_list):
        for _ in range(3):
            three_word_list.next()
        assert three_word_list.complete is True
        three_word_list.reset()
        assert three_word_list.complete is False

    def test_returns_to_first_word(self, three_word_list):
        three_word_list.next()
        three_word_list.next()
        three_word_list.reset()
        assert three_word_list.get_current_word() == "one"

    def test_reset_then_traverse_again(self, three_word_list):
        for _ in range(3):
            three_word_list.next()
        three_word_list.reset()
        words = [three_word_list.get_current_word()]
        three_word_list.next()
        words.append(three_word_list.get_current_word())
        three_word_list.next()
        words.append(three_word_list.get_current_word())
        assert words == ["one", "two", "three"]

    def test_reset_single_word_list(self, single_word_list):
        single_word_list.next()
        single_word_list.reset()
        assert single_word_list.cur_index == 0
        assert single_word_list.remaining == 0
        assert single_word_list.complete is False


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------

class TestRepr:
    def test_repr_contains_cur_index(self, three_word_list):
        assert "cur_index" in repr(three_word_list)

    def test_repr_contains_remaining(self, three_word_list):
        assert "remaining" in repr(three_word_list)

    def test_repr_contains_current_word(self, three_word_list):
        assert "one" in repr(three_word_list)

    def test_repr_is_string(self, three_word_list):
        assert isinstance(repr(three_word_list), str)
