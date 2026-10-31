# PES1UG24CS662_DHANUSH
# Lab 6 - Code (line) coverage test cases for visa_application.py
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- visa_fee ----------------

def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_gets_extra_included_entry():
    # business: 3 included + 1 for group A = 4, so 4 entries are free
    assert visa_fee("business", 4, "normal", "A") == 0


def test_normal_speed_few_extra_entries():
    # tourist: 1 included, 4 entries -> 3 extra at 40
    assert visa_fee("tourist", 4, "normal", "B") == 120


def test_express_many_extra_entries():
    # tourist: 1 included, 8 entries -> 7 extra, rate 100 + 20 + 10 = 130
    assert visa_fee("tourist", 8, "express", "B") == 910


# ---------------- documents_complete ----------------

def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_renewal_with_one_form():
    assert documents_complete(1, 0, True) is True


def test_too_few_photos():
    assert documents_complete(3, 1, False) is False


# ---------------- application_status ----------------

def test_status_open_express():
    # express cutoff 10
    assert application_status(10, True, False) == "open"


def test_status_closing_peak_season():
    # normal cutoff 30 + 15 peak = 45; closing range is 30..44
    assert application_status(30, False, True) == "closing"


def test_status_closed():
    # normal cutoff 30; closed below 15
    assert application_status(5, False, False) == "closed"
