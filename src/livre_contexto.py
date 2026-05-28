import sys


class ContextFreeValidator:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2'}
        self.alphabet = {'BEGIN', 'END'}
        self.stack_alphabet = {'Z0', 'B'}
        self.initial_state = 'q0'
        self.initial_stack = 'Z0'
        self.final_states = {'q2'}

        self.transitions = {
            ('q0', 'BEGIN', 'Z0'): ('q1', ['Z0', 'B']),
            ('q1', 'BEGIN', 'B'): ('q1', ['B', 'B']),
            ('q1', 'END', 'B'): ('q1', []),
            ('q1', '', 'Z0'): ('q2', ['Z0'])
        }

    def recognize(self, string_input: str, verbose=True) -> tuple[bool, int]:
        tokens = string_input.strip().split()
        current_state = self.initial_state
        stack = [self.initial_stack]
        steps = 0

        if verbose:
            print("--- Running LLC Validator ---")

        for token in tokens:
            if not stack or token not in self.alphabet:
                return False, steps

            stack_top = stack.pop()
            key = (current_state, token, stack_top)

            if key in self.transitions:
                next_state, to_push = self.transitions[key]
                steps += 1
                stack.extend(to_push)

                if verbose:
                    print(f"Step {steps}: Read '{token}', Pop '{
                          stack_top}' -> State {next_state}, Stack {stack}")

                current_state = next_state
            else:
                steps += 1
                return False, steps

        if stack:
            stack_top = stack.pop()
            epsilon_key = (current_state, '', stack_top)

            if epsilon_key in self.transitions:
                next_state, to_push = self.transitions[epsilon_key]
                steps += 1
                current_state = next_state
                stack.extend(to_push)

        is_accepted = current_state in self.final_states
        if verbose:
            print(f"Result: {'ACCEPTED' if is_accepted else 'REJECTED'} in {
                  steps} steps.\n")

        return is_accepted, steps


if __name__ == "__main__":
    validator = ContextFreeValidator()
    test_str = " ".join(sys.argv[1:]) if len(
        sys.argv) > 1 else "BEGIN BEGIN END END"

    validator.recognize(test_str)
