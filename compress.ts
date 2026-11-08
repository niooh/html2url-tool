import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { basename, dirname, join } from 'node:path';
import { parseArgs } from 'node:util';
import { minify as minifyJs } from 'oxc-minify';
import { minify as minifyHtml } from 'html-minifier-terser';

const { positionals: [SRC = 'index.html'] } = parseArgs({ allowPositionals: true });
const OUT = join('dist', basename(SRC));

const SCRIPT_RE = /<script(?![^>]*\ssrc\s*=)([^>]*)>([\s\S]*?)<\/script>/gi;

async function minifyInlineScripts(html: string): Promise<string> {
  let out = '';
  let last = 0;

  for (const m of html.matchAll(SCRIPT_RE)) {
    const [full, attrs, code] = m;
    const start = m.index!;
    out += html.slice(last, start);
    last = start + full.length;

    const res = await minifyJs('inline.js', code, { compress: true, mangle: true });
    out += `<script${attrs}>${res.code.replace(/<\/script/gi, '<\\/script')}</script>`;
  }

  return out + html.slice(last);
}

async function main() {
  const html = await readFile(SRC, 'utf8');
  const withOxc = await minifyInlineScripts(html);

  const finalHtml = await minifyHtml(withOxc, {
    collapseWhitespace: true,
    collapseBooleanAttributes: true,
    removeComments: true,
    removeAttributeQuotes: true,
    removeRedundantAttributes: true,
    removeEmptyAttributes: true,
    removeOptionalTags: true,
    useShortDoctype: true,
    sortAttributes: true,
    sortClassName: true,
    minifyCSS: true,
    minifyJS: true,
    minifyURLs: true,
  });

  await mkdir(dirname(OUT), { recursive: true });
  await writeFile(OUT, finalHtml, 'utf8');
  console.log(`${SRC} -> ${OUT}  ${html.length} -> ${finalHtml.length} bytes`);
}

main().catch((e) => { console.error(e); process.exit(1); });
