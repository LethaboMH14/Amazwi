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
const allowedLanguages = new Set(["zu", "tn"]);
const allowedReviewStatuses = new Set(["REVIEWED", "NEEDS_NATIVE_CONFIRMATION"]);

const normalise = (value) => value.normalize("NFC").toLocaleLowerCase().trim().replace(/[\s-]+/gu, " ");

if (!Array.isArray(cards) || cards.length !== 8) {
  errors.push(`hero_8 must contain exactly 8 cards; found ${Array.isArray(cards) ? cards.length : "none"}`);
}

if (typeof data.language !== "string" || !allowedLanguages.has(data.language)) {
  errors.push(`deck language must be one of: ${[...allowedLanguages].join(", ")}`);
}

const review = data.review;
if (!review || typeof review !== "object" || Array.isArray(review)) {
  errors.push("deck review metadata is required");
} else {
  if (!allowedReviewStatuses.has(review.status)) {
    errors.push(`deck review.status must be one of: ${[...allowedReviewStatuses].join(", ")}`);
  }
  if (typeof review.owner !== "string" || !review.owner.trim()) {
    errors.push("deck review.owner must be a non-empty string");
  }
  if (!Array.isArray(review.pending_items) || review.pending_items.some((item) => typeof item !== "string" || !item.trim())) {
    errors.push("deck review.pending_items must be an array of non-empty strings");
  } else if (review.status === "REVIEWED" && review.pending_items.length > 0) {
    errors.push("a REVIEWED deck cannot have pending review items");
  } else if (review.status === "NEEDS_NATIVE_CONFIRMATION") {
    if (review.pending_items.length === 0) {
      errors.push("a NEEDS_NATIVE_CONFIRMATION deck must name at least one pending review item");
    } else {
      warnings.push(`native confirmation pending: ${review.pending_items.join("; ")}`);
    }
  }
}

const seenIds = new Set();

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

  if (typeof card.id !== "string" || !card.id.trim()) {
    errors.push("card id is required");
  } else if (seenIds.has(card.id)) {
    errors.push(`${label}: duplicate card id`);
  } else {
    seenIds.add(card.id);
  }
  if (typeof card.language !== "string" || !allowedLanguages.has(card.language)) {
    errors.push(`${label}: language must be one of: ${[...allowedLanguages].join(", ")}`);
  } else if (card.language !== data.language) {
    errors.push(`${label}: language ${card.language} does not match deck language ${data.language}`);
  }
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
}

console.log(JSON.stringify({ file: path.normalize(file), cards: Array.isArray(cards) ? cards.length : 0, errors, warnings }, null, 2));
process.exit(errors.length ? 1 : 0);
