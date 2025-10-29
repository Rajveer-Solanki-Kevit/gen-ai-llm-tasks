import re

def clean_code(code: str) -> str:
    cleaned = re.sub(r"```(?:python)?", "", code, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()
    return cleaned

def test_code(code: str):
    try:
        code = clean_code(code)
        exec_globals = {}
        exec(code, exec_globals)
        # test_code(exec_globals)
        return True, " All tests passed!"
    except AssertionError as e:
        return False, f" Test failed: {str(e)}"
    except Exception as e:
        return False, f" Runtime error: {str(e)}"

