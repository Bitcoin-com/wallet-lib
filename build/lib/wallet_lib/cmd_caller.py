import subprocess

class CMDCallerResponse:

    def __init__(self, result, error, code):
        self.result = result
        self.error = error
        self.code = code

class CMDCaller:

    def __init__(self, program_name):
        self.program_name = program_name

    def run(self, command, *args):
        proc = subprocess.Popen(self._build_args(command, *args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate(timeout=10)
        return CMDCallerResponse(o.decode('ascii').strip(), e.decode('ascii').strip(), proc.returncode)

    def _build_args(self, command, *args):
        return [self.program_name, command, *args]