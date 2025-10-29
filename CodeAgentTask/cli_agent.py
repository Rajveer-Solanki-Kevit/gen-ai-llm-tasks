from codegen.generator import generate_code
from codegen.tester import test_code

def cli_code_generator():
    print("=== Minimal AI Code Generation Agent ===\n")

    task = input(" Enter your coding task (e.g. write factorial function): ").strip()

    prompt = f"""
    You are an expert Python developer.
    Write a Python function for the following task:
    {task}
    
    The code must define a valid function name.
    Only output valid Python code, no explanations.
    """

    code = generate_code(prompt)
    print("\n=== Generated Code ===\n")
    print(code)

    print("\n=== Running Tests ===")
    passed, feedback = test_code(code)
    print(feedback)

    max_attempts = 3
    attempts = 1
    while not passed and attempts < max_attempts:
        attempts += 1
        print(f"\n Attempt {attempts}: Retrying with feedback...")

        new_prompt = f"""
        Previous code failed tests with this feedback: {feedback}
        Please fix the issues and generate a corrected version of the factorial function.
        Only output Python code.
        """

        code = generate_code(new_prompt)
        print("\n=== Regenerated Code ===\n")
        print(code)

        passed, feedback = test_code(code)
        print(feedback)

    if passed:
        print("\n Success!")
    else:
        print("\n Failed.")

if __name__ == "__main__":
    cli_code_generator()
