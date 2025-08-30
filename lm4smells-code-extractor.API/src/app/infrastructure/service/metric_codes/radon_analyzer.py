import subprocess
import json

class RadonAnalyzer:
    def analyze(self, code: str) -> dict:
        commands = {
            "raw": ["radon", "raw", "-j", "-"],
            "cc":  ["radon", "cc", "-j", "-"],
            "mi":  ["radon", "mi", "-j", "-"],
            "hal": ["radon", "hal", "-j", "-"]
        }

        results = {}
        for name, command in commands.items():
            try:
                results[name] = self.execute_command(command, code)
            except Exception as e:
                results[name] = {"error": str(e)}

        return results

    def execute_command(self, command: list, code: str) -> dict:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=code)

        if process.returncode == 0:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                return {"error": f"Failed to parse JSON output: {stdout}"}
        else:
            raise RuntimeError(f"Error executing command {' '.join(command)}: {stderr}")