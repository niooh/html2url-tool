import argparse
import base64
import os
import pathlib
import re
import sys
import zlib

_ANSI = re.compile(r'\x1b\[[0-9;]*m')
_COLOR = sys.stdout.isatty() and 'NO_COLOR' not in os.environ

def blue(s: str) -> str:
    return f'\033[34m{s}\033[0m' if _COLOR else s

class ColorHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return blue(metavar)
        parts = ', '.join(blue(o) for o in action.option_strings)
        if action.nargs != 0:
            args = self._format_args(
                action, self._get_default_metavar_for_optional(action))
            parts += ' ' + blue(args)
        return parts

    def add_argument(self, action):
        if action.help is not argparse.SUPPRESS:
            w = len(_ANSI.sub('', self._format_action_invocation(action)))
            self._action_max_length = max(
                self._action_max_length, w + self._current_indent
            )
            self._add_item(self._format_action, [action])

def main() -> None:
    ap = argparse.ArgumentParser(
        prog='pack.py',
        description='Pack an HTML file into a self-extracting URL for .html',
        epilog='example:\n  python pack.py page.html --base https://example.com/index.html',
        formatter_class=ColorHelpFormatter,
    )
    ap.add_argument('input', metavar='FILE',
                    help='HTML file to pack')
    ap.add_argument('--base', required=True, metavar='URL',
                    help='URL of .html; payload is appended as #fragment')
    ap.add_argument('-o', '--out', metavar='FILE',
                    help='write the resulting URL to a file')
    a = ap.parse_args()

    src = pathlib.Path(a.input).read_bytes()
    c = zlib.compressobj(9, zlib.DEFLATED, -15)  # raw deflate
    packed = c.compress(src) + c.flush()

    payload = base64.urlsafe_b64encode(packed).decode().rstrip('=')
    url = f"{a.base}#{payload}"

    if a.out:
        pathlib.Path(a.out).write_text(url, encoding='utf-8')

    print(url)


if __name__ == '__main__':
    main()
