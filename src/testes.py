import os
from .regular import RegularValidator
from .livre_contexto import ContextFreeValidator
from .recursiva import RecursiveValidator


def run_tests(file_path, validator, validator_name):
    print(f"\n{'='*50}\nTesting {validator_name}\n{'='*50}")
    print(f"{'Input':<40} | {'Expected':<8} | {'Actual':<8} | Steps")
    print('-'*75)

    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue

                # Formato esperado no txt: "LOGIN AUTH LOGOUT ; ACCEPT"
                parts = line.strip().split(';')
                if len(parts) != 2:
                    continue

                test_str = parts[0].strip()
                expected = parts[1].strip().upper()

                actual_bool, steps = validator.recognize(
                    test_str, verbose=False)
                actual = "ACCEPT" if actual_bool else 'REJECT'

                match = "✅" if expected == actual else '❌'

                print(f"{test_str[:38]:<40} | {expected:<8} | {
                      actual:<8} | {steps} {match}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.join(base_dir, "testes")

    run_tests(os.path.join(test_dir, "testes_regular.txt"),
              RegularValidator(), "Regular Language (DFA)")
    run_tests(os.path.join(test_dir, "testes_livre_contexto.txt"),
              ContextFreeValidator(), "Context-Free (PDA)")
    run_tests(os.path.join(test_dir, "testes_recursiva.txt"),
              RecursiveValidator(), "Recursive (Turin Machine)")
