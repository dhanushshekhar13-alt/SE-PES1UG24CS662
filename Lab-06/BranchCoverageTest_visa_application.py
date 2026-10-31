# PES1UG24CS662_DHANUSH
# Lab 6 - Branch coverage test cases for visa_application.py
# Every if/else decision is exercised on both its True and False side.
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------- visa_fee ----------------

# if visa_type not in INCLUDED_ENTRIES -> True / False
def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "B")


def test_known_visa_type_accepted():
    assert visa_fee("tourist", 1, "normal", "B") == 0


# if entries < 0 -> True / False (boundary: -1 vs 0)
def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("business", -1, "normal", "B")


def test_zero_entries_is_free():
    assert visa_fee("business", 0, "normal", "B") == 0


# if nationality_group == "A" and visa_type != "student"
def test_group_a_non_student_gets_extra_entry():
    # business: 3 + 1 = 4 included
    assert visa_fee("business", 4, "normal", "A") == 0
    assert visa_fee("business", 5, "normal", "A") == 40


def test_group_a_student_gets_no_extra_entry():
    # student: 2 included, no bonus -> 1 extra at 40
    assert visa_fee("student", 3, "normal", "A") == 40


def test_group_b_gets_no_extra_entry():
    # tourist: 1 included -> 1 extra at 40
    assert visa_fee("tourist", 2, "normal", "B") == 40


# if extra <= 0 -> True / False (boundary: extra == 0 vs extra == 1)
def test_extra_exactly_zero_is_free():
    assert visa_fee("student", 2, "express", "B") == 0


def test_extra_exactly_one_is_charged():
    assert visa_fee("student", 3, "express", "B") == 100


# if speed == "express" -> True / False, with extra <= 5 (inner bonus skipped)
def test_express_few_extra_entries():
    # tourist: 5 extra at 100
    assert visa_fee("tourist", 6, "express", "B") == 500


def test_normal_few_extra_entries():
    # tourist: 5 extra at 40
    assert visa_fee("tourist", 6, "normal", "B") == 200


# if extra > 5 -> True, inner if speed == "express" -> True / False
def test_express_many_extra_entries():
    # tourist: 6 extra, rate 100 + 20 + 10 = 130
    assert visa_fee("tourist", 7, "express", "B") == 780


def test_normal_many_extra_entries():
    # tourist: 6 extra, rate 40 + 20 = 60
    assert visa_fee("tourist", 7, "normal", "B") == 360


# ---------------- documents_complete ----------------

# if is_renewal -> True (both outcomes of forms_filed >= 1)
def test_renewal_with_one_form():
    assert documents_complete(1, 0, True) is True


def test_renewal_with_no_forms():
    assert documents_complete(0, 5, True) is False


# if is_renewal -> False, if photos < 2 -> True
def test_new_application_too_few_photos():
    assert documents_complete(3, 1, False) is False


# if photos < 2 -> False (both outcomes of forms_filed >= 3)
def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_new_application_too_few_forms():
    assert documents_complete(2, 2, False) is False


# ---------------- application_status ----------------

# is_express True / False x is_peak_season True / False,
# plus each of the three outcomes (open / closing / closed)

def test_express_off_peak_open():
    # cutoff 10
    assert application_status(10, True, False) == "open"


def test_express_off_peak_closed():
    # cutoff 10, closing needs >= -5, so -6 is closed
    assert application_status(-6, True, False) == "closed"


def test_express_peak_closing():
    # cutoff 25, closing range 10..24
    assert application_status(10, True, True) == "closing"


def test_normal_off_peak_open():
    # cutoff 30
    assert application_status(30, False, False) == "open"


def test_normal_off_peak_closing_boundary():
    # cutoff 30, closing range 15..29
    assert application_status(29, False, False) == "closing"
    assert application_status(15, False, False) == "closing"


def test_normal_off_peak_closed():
    assert application_status(14, False, False) == "closed"


def test_normal_peak_open():
    # cutoff 45
    assert application_status(45, False, True) == "open"


def test_normal_peak_closing():
    assert application_status(30, False, True) == "closing"


def test_normal_peak_closed():
    assert application_status(29, False, True) == "closed"
