# html2url-tool

Pack a whole HTML page into a URL.

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

   The URL is written to `url.txt` and printed.

3. Open the URL in a browser.

## Options

| Flag           | Meaning                                              |
| -------------- | ---------------------------------------------------- |
| `--base URL`   | URL of `index.html`; payload is appended as `#fragment` |
| `-o, --out`    | Output file (default `url.txt`)                      |

## Limits

- Long URLs may get truncated by browsers and chat apps.
- The packed page is sandboxed: no cookies, no `localStorage` of the host.
