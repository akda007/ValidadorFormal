import sys


class RecursiveValidator:
    def __init__(self):
        self.blank = "_"
        self.alphabet = {'OPEN', 'COMMIT', "CLOSE"}
        self.tape_alphabet = {
            'OPEN',
            "COMMIT",
            "CLOSE",
            "X", "Y", "Z",
            self.blank
        }

        self.initial_state = 'q0'
        self.final_states = {'q_accept'}

        self.transitions = {
            ('q0', 'OPEN'): ('q1', 'X', 'R'),

            ('q1', 'OPEN'): ('q1', 'OPEN', 'R'),
            ('q1', 'Y'): ('q1', 'Y', 'R'),

            ('q1', 'COMMIT'): ('q2', 'Y', 'R'),

            ('q2', 'COMMIT'): ('q2', 'COMMIT', 'R'),
            ('q2', 'Z'): ('q2', 'Z', 'R'),

            ('q2', 'CLOSE'): ('q3', 'Z', 'L'),

            ('q3', 'Z'): ('q3', 'Z', 'L'),
            ('q3', 'COMMIT'): ('q3', 'COMMIT', 'L'),
            ('q3', 'Y'): ('q3', 'Y', 'L'),
            ('q3', 'OPEN'): ('q3', 'OPEN', 'L'),
            ('q3', 'X'): ('q0', 'X', 'R'),

            ('q0', 'Y'): ('q4', 'Y', 'R'),
            ('q4', 'Y'): ('q4', 'Y', 'R'),
            ('q4', 'Z'): ('q4', 'Z', 'R'),

            ('q4', self.blank): ('q_accept', self.blank, 'R')
        }

    def recognize(self, string_input: str, verbose=True) -> tuple[bool, int]:
        if not string_input.strip():
            return False, 0

        tape = string_input.strip().split()
        head = 0
        current_state = self.initial_state
        steps = 0

        if verbose:
            print("--- Running Recursive (TM) Validator ---")

        while current_state not in self.final_states:
            if head == len(tape):
                tape.append(self.blank)
            elif head < 0:
                tape.insert(0, self.blank)
                head = 0

            read_symbol = tape[head]
            key = (current_state, read_symbol)

            if key in self.transitions:
                next_state, write_symbol, direction = self.transitions[key]
                tape[head] = write_symbol
                steps += 1

                if verbose:
                    print(f"Step {steps}: State {current_state} read '{
                          read_symbol}' -> Write '{write_symbol}', Move {direction}, State {next_state}")

                current_state = next_state
                head += 1 if direction == "R" else -1
            else:
                steps += 1
                if verbose:
                    print(f"Rejected at step {steps}: No transition for state '{
                          current_state}' and symbol '{read_symbol}'")
                return False, steps

        is_accepted = current_state in self.final_states
        if verbose:
            print(f"Result: {'ACCEPTED' if is_accepted else 'REJECTED'} in {
                  steps} steps.\n")

        return is_accepted, steps


if __name__ == "__main__":
    validator = RecursiveValidator()
    test_str = " ".join(sys.argv[1:]) if len(
        sys.argv) > 1 else "OPEN COMMIT CLOSE"

    validator.recognize(test_str)
