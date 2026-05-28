import re
import time
from .regular import RegularValidator


def compare_regex_vs_dfa(test_string):
    print(f"{'='*60}\nComparing Manual DFA vs Python 're' Module\n{'='*60}")
    print(f"Input String: '{test_string}'\n")

    # 1. Test manual DFA
    dfa = RegularValidator()
    start_dfa = time.perf_counter()
    is_accepted_dfa, steps = dfa.recognize(test_string, verbose=False)
    end_dfa = time.perf_counter()
    time_dfa = (end_dfa - start_dfa) * 1000

    print("--- Manual DFA ---")
    print(f"Result: {'ACCEPTED' if is_accepted_dfa else 'REJECTED'}")
    print(f"Steps taken: {steps}")
    print(f"Execution time: {time_dfa:.5f} ms\n")

    # 2. Python Regex Test
    pattern = re.compile(r'^LOGIN AUTH( REQUEST)* LOGOUT$')

    start_re = time.perf_counter()
    match = pattern.match(test_string)
    is_accepted_re = bool(match)
    end_re = time.perf_counter()
    time_re = (end_re - start_re) * 1000

    print("--- Python 're' Module ---")
    print(f"Result: {'ACCEPTED' if is_accepted_re else 'REJECTED'}")
    print("Engine steps: Hidden (Compiled in C)")
    print(f"Execution time: {time_re:.5f} ms\n")

    print("--- Analysis ---")
    if time_re < time_dfa:
        print("Conclusion: The 're' module is faster because it is pre-compiled in C.")
    else:
        print(
            "Conclusion: The manual DFA was faster for this specific short string overhead.")

    print("However, the manual DFA allows us to mathematically count the exact state transitions (steps).")


if __name__ == "__main__":
    massive_requests = " REQUEST" * 1000
    test_str = f"LOGIN AUTH{massive_requests} LOGOUT"
    compare_regex_vs_dfa(test_str)
