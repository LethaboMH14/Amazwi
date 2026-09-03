/**
 * AMAZWI's mascot: the two listeners.
 *
 * Deliberately NOT a generic robot. The reference dashboards anchor
 * themselves with a 3D character, and that anchor works -- but bolting
 * an unrelated mascot onto this product would be decoration with no
 * meaning behind it.
 *
 * AMAZWI already has a signature device: two overlapping circles, one
 * warm and one cool, because TWO PEOPLE AGREEING IS THE MECHANIC. This
 * gives that device a face. The mascot is therefore the product's own
 * logic drawn as a character, not an ornament placed beside it.
 *
 * Built as inline SVG with layered gradients rather than a raster 3D
 * render: it scales to any size, recolours with the theme, adds zero
 * bytes to the bundle beyond its own markup, and stays crisp on the
 * cheap Android screens this product is actually for.
 *
 * `mood` reflects real state and nothing else:
 *   idle       -- default
 *   listening  -- a recording is in progress
 *   understood -- both peers agreed (the eyes curve into a smile)
 *   missed     -- peers disagreed. NOT a sad or scolding face: nobody
 *                 failed, two people simply heard differently, and the
 *                 product must never make a contributor feel punished
 *                 for an outcome that protects the corpus.
 */
import type { CSSProperties } from "react";
import "./mascot.css";

export type MascotMood = "idle" | "listening" | "understood" | "missed";

export function Mascot({
  size = 108,
  mood = "idle",
  className,
  style,
}: {
  size?: number;
  mood?: MascotMood;
  className?: string;
  style?: CSSProperties;
}) {
  const label = {
    idle: "Two listeners, waiting",
    listening: "Two listeners, listening",
    understood: "Two listeners, both understood you",
    missed: "Two listeners, they heard differently",
  }[mood];

  return (
    <svg
      className={`mascot mascot-${mood}${className ? ` ${className}` : ""}`}
      style={style}
      width={size}
      height={size * 0.78}
      viewBox="0 0 140 110"
      role="img"
      aria-label={label}
    >
      <defs>
        {/* Warm listener. The inner highlight sits top-left and the core
            shadow bottom-right -- the same light model as the clay cards,
            so the mascot belongs to the same world. */}
        <radialGradient id="mascot-warm" cx="32%" cy="26%" r="82%">
          <stop offset="0%" stopColor="#F6B08A" />
          <stop offset="52%" stopColor="#E8894A" />
          <stop offset="100%" stopColor="#B8551F" />
        </radialGradient>
        <radialGradient id="mascot-cool" cx="34%" cy="26%" r="82%">
          <stop offset="0%" stopColor="#A9C0E6" />
          <stop offset="52%" stopColor="#6E8FC6" />
          <stop offset="100%" stopColor="#3D5E96" />
        </radialGradient>
        <radialGradient id="mascot-shadow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgba(7,58,3,0.30)" />
          <stop offset="100%" stopColor="rgba(7,58,3,0)" />
        </radialGradient>
      </defs>

      {/* Contact shadow -- what makes it sit in the scene rather than
          float in front of it. */}
      <ellipse cx="70" cy="99" rx="44" ry="7" fill="url(#mascot-shadow)" />

      {/* Cool listener, behind. */}
      <g className="mascot-listener mascot-listener-b">
        <circle cx="88" cy="52" r="34" fill="url(#mascot-cool)" />
        <ellipse cx="76" cy="36" rx="14" ry="9" fill="rgba(255,255,255,0.30)" transform="rotate(-24 76 36)" />
        <g className="mascot-eyes">
          <circle className="mascot-eye" cx="84" cy="50" r="3.6" fill="#12233F" />
          <circle className="mascot-eye" cx="99" cy="50" r="3.6" fill="#12233F" />
          <path className="mascot-smile" d="M83 61q8.5 6 17 0" stroke="#12233F" strokeWidth="2.6" strokeLinecap="round" fill="none" />
        </g>
      </g>

      {/* Warm listener, in front. */}
      <g className="mascot-listener mascot-listener-a">
        <circle cx="52" cy="56" r="37" fill="url(#mascot-warm)" />
        <ellipse cx="39" cy="38" rx="15" ry="10" fill="rgba(255,255,255,0.34)" transform="rotate(-24 39 38)" />
        <g className="mascot-eyes">
          <circle className="mascot-eye" cx="45" cy="54" r="4" fill="#3A1405" />
          <circle className="mascot-eye" cx="62" cy="54" r="4" fill="#3A1405" />
          <path className="mascot-smile" d="M44 66q9 6.5 18 0" stroke="#3A1405" strokeWidth="2.8" strokeLinecap="round" fill="none" />
        </g>
      </g>

      {/* Sound arcs, only drawn while listening. */}
      <g className="mascot-waves" aria-hidden="true">
        <path d="M120 40q9 12 0 24" stroke="var(--voice-1, #067A43)" strokeWidth="2.6" strokeLinecap="round" fill="none" opacity="0.75" />
        <path d="M128 32q15 20 0 40" stroke="var(--voice-1, #067A43)" strokeWidth="2.6" strokeLinecap="round" fill="none" opacity="0.45" />
      </g>
    </svg>
  );
}
