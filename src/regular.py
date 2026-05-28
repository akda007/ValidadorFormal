import sys


class RegularValidator:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'LOGIN', 'AUTH', 'REQUEST', 'LOGOUT'}
        self.initial_state = 'q0'
        self.final_state = {'q3'}

        self.transitions = {
            'q0': {'LOGIN': 'q1'},
            'q1': {'AUTH': 'q2'},
            'q2': {'REQUEST': 'q2', 'LOGOUT': 'q3'},
            'q3': {},
        }

    def recognize(self, string_input: str, verbose=True) -> tuple[bool, int]:
        tokens = string_input.strip().split()
        current_state = self.initial_state
        steps = 0

        if verbose:
            print("--- Running LR Validadtor ---")

        for token in tokens:
            if token not in self.alphabet:
                if verbose:
                    print(f"Rejected: Token '{token}' not in alphabet.")
                    return False, steps

            if token in self.transitions[current_state]:
                next_state = self.transitions[current_state][token]
                steps += 1

                if verbose:
                    print(f"Step {steps}: '{token}' -> state {next_state}")

                current_state = next_state
            else:
                steps += 1
                if verbose:
                    print(f"Rejected at step {steps}: Invalid token '{
                          token}' for state '{current_state}'")
                return False, steps

        is_accepted = current_state in self.final_state
        if verbose:
            print(
                f"Result: {'ACCEPTED' if is_accepted else 'REJECTED'} in {
                    steps} steps."
            )

        return is_accepted, steps


if __name__ == "__main__":
    validator = RegularValidator()
    test_str = " ".join(sys.argv[1:]) if len(
        sys.argv) > 1 else "LOGIN AUTH REQUEST LOGOUT"

    validator.recognize(test_str)
