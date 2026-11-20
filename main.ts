// main.ts — copy entry.png to the output directory and verify the copy.
//
// Usage: node main.ts
// Output directory: MAKEFUN_OUTPUT_DIR, or /output when that is not set.
// Only the Node standard library is used.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const repoDir = new URL(".", import.meta.url).pathname;
const source = join(repoDir, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found at ${source}`);
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");

copyFileSync(source, dest);

const original = readFileSync(source);
const copied = readFileSync(dest);
if (!original.equals(copied)) {
  console.error("entry.png copy differs from the original; refusing to continue");
  process.exit(1);
}

console.log(`copied entry.png to ${dest} (${copied.length} bytes, byte-identical)`);
