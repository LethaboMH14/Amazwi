import fs from "node:fs";

const file = process.argv[2] ?? "05_amazwi/content/error_states.json";
const data = JSON.parse(fs.readFileSync(file, "utf8"));
const expected = [
  "mic_denied",
  "browser_unsupported",
  "upload_network_failure",
  "no_verifiers_available",
  "contribution_waiting_or_expired",
  "consent_revoked",
  "campaign_empty",
  "provider_unavailable",
  "cash_out_failed",
  "duplicate_action_ignored"
];
const languages = ["en", "zu", "tn"];
const errors = [];

const actual = Object.keys(data).filter((key) => key !== "_meta");
for (const state of expected) if (!actual.includes(state)) errors.push(`missing state: ${state}`);
for (const state of actual) if (!expected.includes(state)) errors.push(`unexpected state: ${state}`);

for (const state of expected) {
  const entry = data[state];
  if (!entry) continue;
  const retryValues = [];
  for (const language of languages) {
    const copy = entry[language];
    if (!copy || typeof copy !== "object") {
      errors.push(`${state}.${language}: copy object is required`);
      continue;
    }
    for (const field of ["title", "body", "action"]) {
      if (typeof copy[field] !== "string" || !copy[field].trim()) errors.push(`${state}.${language}.${field}: non-empty string required`);
    }
    if (typeof copy.retryable !== "boolean") errors.push(`${state}.${language}.retryable: boolean required`);
    else retryValues.push(copy.retryable);
  }
  if (new Set(retryValues).size > 1) errors.push(`${state}: retryable must agree across languages`);
}

console.log(JSON.stringify({ file, states: actual.length, languages, errors }, null, 2));
process.exit(errors.length ? 1 : 0);
