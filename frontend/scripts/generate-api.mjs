import { mkdir, readFile, writeFile } from "node:fs/promises";
import openapiTS, { astToString } from "openapi-typescript";

const schema = new URL("../../contracts/openapi.json", import.meta.url);
const destination = new URL("../src/lib/api.generated.ts", import.meta.url);
const header =
  "/** Generated from contracts/openapi.json. Run npm run api:generate; do not edit. */\n";

const ast = await openapiTS(schema);
const generated = header + astToString(ast);

if (process.argv.includes("--check")) {
  let existing;
  try {
    existing = await readFile(destination, "utf8");
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  // Git may check out CRLF on Windows; line endings carry no schema information.
  if (existing?.replace(/\r\n/g, "\n") !== generated) {
    console.error("API types are stale. Export OpenAPI, then run npm run api:generate.");
    process.exitCode = 1;
  } else {
    console.log("Generated API types match contracts/openapi.json.");
  }
} else {
  await mkdir(new URL("../src/lib/", import.meta.url), { recursive: true });
  await writeFile(destination, generated);
  console.log("Generated src/lib/api.generated.ts from contracts/openapi.json.");
}
