import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const compiledPath = join(here, "amazwi-mockups-v2.html");
const compiled = await readFile(compiledPath, "utf8");
const checkOnly = process.argv.includes("--check");
const payloadPattern = /(<script type="application\/json" id="appifact-doc">\s*)([\s\S]*?)(\s*<\/script>)/;
const match = compiled.match(payloadPattern);

if (!match) {
  throw new Error("Could not find the appifact-doc payload in amazwi-mockups-v2.html");
}

const document = JSON.parse(match[2]);
const fileNames = Object.keys(document?.content?.files ?? {});

for (const fileName of fileNames) {
  if (fileName === "canvas.json" || fileName.endsWith(".dc.html")) {
    document.content.files[fileName] = await readFile(join(here, fileName), "utf8");
  }
}

const payload = JSON.stringify(document)
  .replaceAll("<", "\\u003c")
  .replaceAll("\u2028", "\\u2028")
  .replaceAll("\u2029", "\\u2029");
const stamp = createHash("md5").update(payload).digest("hex");
const withPayload = compiled.replace(payloadPattern, `$1${payload}$3`);
const output = withPayload.replace(
  /<meta name="mega-build-stamp" content="[^"]+">/,
  `<meta name="mega-build-stamp" content="${stamp}">`,
);

if (checkOnly) {
  if (output !== compiled) {
    console.error("amazwi-mockups-v2.html is stale; run node reseed_compiled.mjs");
    process.exitCode = 1;
  } else {
    console.log(`Compiled canvas is in sync with ${fileNames.length} source files (${stamp}).`);
  }
} else {
  await writeFile(compiledPath, output, "utf8");
  console.log(`Reseeded ${fileNames.length} canvas files into amazwi-mockups-v2.html (${stamp}).`);
}
