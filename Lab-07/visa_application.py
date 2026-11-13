import math

def parse_application(text):
    try:
        if not isinstance(text, str):
            return None
        parts = text.split(':')
        if len(parts) != 2:
            return None
        visa, entries = parts
        visa = visa.strip().title()
        if not visa:
            return None
        return visa, int(entries.strip())
    except Exception:
        return None

def processing_average(days_csv):
    try:
        if not isinstance(days_csv, str):
            return 0
        values = [int(r.strip()) for r in days_csv.split(',') if r.strip()]
        if not values:
            return 0
        return sum(values) // len(values)
    except Exception:
        return 0

def payable_fee(text):
    try:
        if not isinstance(text, str):
            return 0.0
        parts = text.split('|')
        if len(parts) != 2:
            return 0.0
        fee, discount = parts
        f_fee = float(fee.strip())
        f_disc = float(discount.strip())
        if math.isnan(f_fee) or math.isnan(f_disc) or math.isinf(f_fee) or math.isinf(f_disc):
            return 0.0
        total = f_fee * 1.18 - f_disc
        return max(total, 0.0)
    except Exception:
        return 0.0

def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)

if __name__ == "__main__":
    main()