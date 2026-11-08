# html2url-tool

A simple tool that packs an HTML page into a URL.

## Install

- Node.js ≥ 22.18.0
- Python ≥ 3.8

```bash
npm install
# or: pnpm install
```

## Usage

1. Optionally minify HTML files:

   ```bash
   npm run build  # index.html -> dist/index.html
   npm run build page.html  # page.html -> dist/page.html
   ```

2. Pack a HTML file into a URL:

   ```bash
   python pack.py page.html --base https://example.com/index.html
   ```

3. The URL is printed, you can open it in a browser.

## Options for pack.py

| Flag         | Meaning             |
| ------------ | ------------------- |
| `--base URL` | URL of `index.html` |
| `-o, --out`  | Output file         |
| `-h, --help` | Show help           |

## Limits

- Long URLs may get truncated by browsers and chat apps.
- The packed page is sandboxed: no cookies, no `localStorage` of the host.
