import fs from "node:fs";
import path from "node:path";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node validate_cards.mjs <cards.json>");
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(file, "utf8"));
const cards = data.hero_8;
const errors = [];
const warnings = [];

const normalise = (value) => value.normalize("NFC").toLocaleLowerCase().trim().replace(/[\s-]+/gu, " ");

if (!Array.isArray(cards) || cards.length !== 8) {
  errors.push(`hero_8 must contain exactly 8 cards; found ${Array.isArray(cards) ? cards.length : "none"}`);
}

for (const card of Array.isArray(cards) ? cards : []) {
  const label = card.id ?? "missing-id";
  const checkList = (field, length) => {
    const values = card[field];
    if (!Array.isArray(values) || values.length !== length || values.some((value) => typeof value !== "string" || !value.trim())) {
      errors.push(`${label}: ${field} must contain exactly ${length} non-empty strings`);
      return [];
    }
    if (new Set(values.map(normalise)).size !== values.length) {
      errors.push(`${label}: ${field} contains duplicate values after normalisation`);
    }
    return values.map(normalise);
  };

  if (typeof card.target !== "string" || !card.target.trim()) errors.push(`${label}: target is required`);
  const blocked = checkList("blocked_words", 4);
  const distractors = checkList("distractors", 3);
  const accepted = Array.isArray(card.accepted_answers) ? card.accepted_answers.map(normalise) : [];

  if (accepted.length < 2 || accepted.some((value) => !value)) {
    errors.push(`${label}: accepted_answers must contain at least 2 non-empty native-reviewed forms`);
  }
  if (new Set(accepted).size !== accepted.length) errors.push(`${label}: accepted_answers contains duplicates after normalisation`);
  if (blocked.some((value) => accepted.includes(value))) errors.push(`${label}: blocked_words overlaps accepted_answers`);
  if (distractors.some((value) => accepted.includes(value))) errors.push(`${label}: distractors overlaps accepted_answers`);
  const blockedDistractors = distractors.filter((value) => blocked.includes(value));
  if (blockedDistractors.length) warnings.push(`${label}: blocked_words also used as distractors: ${blockedDistractors.join(", ")}`);
  if (String(card.confidence ?? "").toLocaleUpperCase().includes("DRAFT")) errors.push(`${label}: confidence is still DRAFT`);
}

if (String(data.status ?? "").toLocaleUpperCase().includes("DRAFT")) {
  errors.push("deck status is still DRAFT");
}

console.log(JSON.stringify({ file: path.normalize(file), cards: Array.isArray(cards) ? cards.length : 0, errors, warnings }, null, 2));
process.exit(errors.length ? 1 : 0);
