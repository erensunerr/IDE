from .trace import Trace

class IDE:
    def __init__(self, initial_text: list[str]):
        self.buffer = initial_text
        self.trace_log: list[Trace] = []
        self.trace_ptr = -1
        self.tools = {}
        self._register_tools()

    def tool(self, func):
        def wrapped(*args, **kwargs):
            trace = Trace(func.__name__, args, kwargs)
            self.trace_log.append(trace)
            self.trace_ptr += 1
            result = func(*args, **kwargs)
            return result

        self.tools[func.__name__] = wrapped
        return func

    def _register_tools(self):
        self.tool(self.replace_line)

    def replace_line(self, line_num: int, new_text: str):
        self.buffer[line_num] = new_text

    def get_context(self):
        return "\n".join(self.buffer)