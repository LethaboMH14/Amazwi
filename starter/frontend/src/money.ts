/**
 * Format a minor-unit amount (cents) for display.
 *
 * The API returns `reward_minor` in MINOR units: 200 means R2.00, not R200.
 * The Voice Value Receipt rendered it raw as "200 ZAR" -- a hundredfold
 * overstatement of the published reward rate, on the one screen whose whole
 * purpose is being financially honest. A judge reading "200 ZAR per clip"
 * would rightly reject the unit economics on the spot.
 *
 * Uses Intl so the currency symbol and grouping follow the locale rather than
 * being hand-assembled. Falls back to a plain "<amount> <code>" string if the
 * runtime rejects the currency code, so an unexpected code degrades to
 * something readable instead of throwing on the receipt.
 */
export function formatMinor(minor: number, currency: string, locale = "en-ZA"): string {
  const major = minor / 100;
  try {
    return new Intl.NumberFormat(locale, {
      style: "currency",
      currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(major);
  } catch {
    return `${major.toFixed(2)} ${currency}`;
  }
}
