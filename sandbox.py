import subprocess
import sys

def run_tool_sandboxed(script_path, timeout=10):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return 'Error: Tool execution timed out.'
    except Exception as e:
        return f'Error: {e}' 