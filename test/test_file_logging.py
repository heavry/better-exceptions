"""Test that file logs are uncolored but stderr keeps colors."""
import io
import logging
import os
import re
import sys
import tempfile

import better_exceptions

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')

def main():
    better_exceptions.SUPPORTS_COLOR = True
    better_exceptions.hook()

    fd, path = tempfile.mkstemp()
    os.close(fd)

    original_stderr = sys.stderr
    terminal = io.StringIO()
    root = logging.getLogger()

    try:
        sys.stderr = terminal
        file_handler = logging.FileHandler(path)
        stream_handler = logging.StreamHandler(sys.stderr)
        logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])

        logger = logging.getLogger(__name__)
        try:
            x = 52
            assert x == 90
        except AssertionError:
            logger.exception("test failed")

        for h in root.handlers:
            h.flush()

        with open(path) as f:
            file_output = f.read()
        terminal_output = terminal.getvalue()

        # File output should NOT have ANSI codes
        assert not ANSI_ESCAPE.search(file_output),             f"File output should not contain ANSI codes: {file_output[:100]}"
        print("PASS: file output has no ANSI codes")

        # stderr output SHOULD have ANSI codes
        assert ANSI_ESCAPE.search(terminal_output),             f"Terminal output should contain ANSI codes: {terminal_output[:100]}"
        print("PASS: terminal output has ANSI codes")
    finally:
        sys.stderr = original_stderr
        for h in root.handlers[:]:
            h.close()
            root.removeHandler(h)
        os.remove(path)

if __name__ == "__main__":
    main()
