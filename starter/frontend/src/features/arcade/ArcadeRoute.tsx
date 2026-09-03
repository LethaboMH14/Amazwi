/**
 * The engagement dashboard.
 *
 * Layout follows the dense desk-style reference: persistent left menu,
 * an overview strip, a deck grid, a leaderboard with a podium, a quest
 * list, and a right rail of invitations and peers. What it does NOT
 * borrow is the reference's palette -- every colour here comes from
 * `tokens.css`, so all five themes and the contrast/zoom evidence in
 * ACCESSIBILITY_EVIDENCE.md keep holding. Hard-coding the reference's
 * teal would have silently voided that work.
 *
 * Two omissions are deliberate and load-bearing:
 *
 *   1. No skill radar. The reference shows five personality axes.
 *      AMAZWI measures none of them, so the same visual slot renders
 *      `outcomes` -- the real understood / not understood / waiting /
 *      closed split from the resolver.
 *   2. No "N playing now". Live presence is not tracked, so each deck
 *      shows a real contributor count instead.
 *
 * Money copy: `earned_cents` is what the ledger has CREDITED. It is not
 * a cash balance and this screen never calls it one -- payout is a
 * separate, reviewed step.
 */
import { useCallback, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import { usePolling } from "../../usePolling";
import type { ArcadeDashboard, LeaderboardRow, QuestRow } from "../../api/contracts";
import { Mascot } from "./Mascot";
import { TabBar } from "./TabBar";
import "./arcade.css";

const LANGUAGE_NAMES: Record<string, string> = { zu: "isiZulu", tn: "Setswana" };

export function languageName(code: string): string {
  return LANGUAGE_NAMES[code] ?? code;
}

export function formatRand(cents: number): string {
  return `R${(cents / 100).toFixed(2)}`;
}

/**
 * Initials for the avatar disc. Decorative only -- never announced.
 *
 * Strips non-letters first: the seeded names carry a language suffix
 * ("Demo Speaker (zu)"), and taking the last word's first character
 * blindly rendered "D(" on the real dashboard.
 */
export function initials(name: string): string {
  const parts = name
    .split(/\s+/)
    .map((part) => part.replace(/[^\p{L}\p{N}]/gu, ""))
    .filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

const NAV_PRIMARY = [
  { to: "/dashboard", label: "Dashboard", icon: "◆" },
  { to: "/rewards", label: "My rewards", icon: "◇" },
  { to: "/impact", label: "Impact map", icon: "◈" },
];


/** Tier ladder, lowest to highest. Mirrors TIER_THRESHOLDS in
 *  app/arcade.py -- the tier itself is earned from verified clips, so
 *  the stars decorate a real achievement rather than invent a score. */
export const TIER_LADDER = [
  "Beginner",
  "Amateur",
  "Veteran",
  "Expert",
  "Master",
  "Grand Master",
] as const;

export function tierIndex(tier: string): number {
  const i = TIER_LADDER.indexOf(tier as (typeof TIER_LADDER)[number]);
  return i < 0 ? 0 : i;
}

function StarIcon({ filled, lead }: { filled: boolean; lead?: boolean }) {
  return (
    <svg
      width="13"
      height="13"
      viewBox="0 0 24 24"
      aria-hidden="true"
      className={`${filled ? "tier-star-filled" : "tier-star-empty"}${lead ? " tier-star-lead" : ""}`}
      fill={filled ? "currentColor" : "none"}
      stroke="currentColor"
      strokeWidth={filled ? 0 : 1.6}
      strokeLinejoin="round"
    >
      <path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.6 1.1 6.5L12 17.5l-5.8 3.05 1.1-6.5-4.7-4.6 6.5-.95z" />
    </svg>
  );
}

/** Stars for a tier. The text label always stays beside them, so the
 *  stars are never the only way to read a rank. */
export function TierStars({ tier }: { tier: string }) {
  const earned = tierIndex(tier) + 1;
  return (
    <span
      className="tier-stars"
      role="img"
      aria-label={`${tier}, ${earned} of ${TIER_LADDER.length}`}
    >
      {TIER_LADDER.map((_, i) => (
        <StarIcon key={i} filled={i < earned} lead={i === earned - 1} />
      ))}
    </span>
  );
}

/**
 * The bubble field.
 *
 * Not decoration pulled from nowhere: `count` is the real number of
 * peer-verified contributions across the decks, so every bubble on
 * screen is a voice two people actually understood. It is capped so a
 * healthy corpus does not become a blizzard.
 */
export function BubbleField({ count }: { count: number }) {
  const shown = Math.min(Math.max(count, 0), 18);
  const bubbles = Array.from({ length: shown }, (_, i) => {
    // Deterministic from the index, so the field does not reshuffle on
    // every re-render and flicker.
    const seed = (i * 2654435761) % 1000;
    return {
      size: 26 + (seed % 58),
      left: (seed * 7) % 96,
      duration: 22 + (seed % 18),
      delay: -((seed * 3) % 30),
      drift: ((seed % 60) - 30) * 1.6,
      opacity: 0.05 + (seed % 7) / 100,
    };
  });

  return (
    <div className="bubbles" aria-hidden="true">
      {bubbles.map((b, i) => (
        <span
          key={i}
          className="bubble"
          style={
            {
              width: `${b.size}px`,
              height: `${b.size}px`,
              left: `${b.left}%`,
              "--bubble-duration": `${b.duration}s`,
              "--bubble-delay": `${b.delay}s`,
              "--bubble-drift": `${b.drift}px`,
              "--bubble-opacity": b.opacity,
            } as React.CSSProperties
          }
        />
      ))}
    </div>
  );
}

/** A short celebratory burst. Emoji here on purpose -- the platform's
 *  own rendering is part of the charm and nothing aligns to it, unlike
 *  the tier stars which sit inline with text. */
export function Burst() {
  const marks = ["\u2728", "\u2B50", "\uD83C\uDF89", "\u2728", "\u2B50"];
  return (
    <span className="burst" aria-hidden="true">
      {marks.map((m, i) => (
        <span
          key={i}
          style={
            {
              "--burst-x": `${(i - 2) * 26 - 8}px`,
              "--burst-y": `${-38 - (i % 3) * 16}px`,
              "--burst-delay": `${i * 70}ms`,
            } as React.CSSProperties
          }
        >
          {m}
        </span>
      ))}
    </span>
  );
}


/** Persistent currency HUD.
 *
 * Every reference dashboard keeps the player's currency on screen at all
 * times. Burying earnings inside one panel was a hierarchy mistake: it
 * is the most motivating number in the product and it should never
 * scroll away. Both values are real -- rand from the reward ledger, XP
 * derived from verified clips. */
export function CurrencyHud({
  earnedCents,
  xp,
}: {
  earnedCents: number;
  xp: number;
}) {
  return (
    <div className="hud">
      <span className="hud-pill">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" className="hud-rand" fill="currentColor">
          <circle cx="12" cy="12" r="9" opacity="0.28" />
          <path d="M12 5.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zm-2 3h2.6a2.2 2.2 0 0 1 0 4.4H11v2.6H10V8.5zm1 1v2.4h1.6a1.2 1.2 0 0 0 0-2.4H11z" />
        </svg>
        {formatRand(earnedCents)}
        <span className="hud-label">credited</span>
      </span>
      <span className="hud-pill">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true" className="hud-xp" fill="currentColor">
          <path d="M12 2.6l2.6 6.2 6.7.55-5.1 4.4 1.55 6.55L12 16.8l-5.75 3.5L7.8 13.75 2.7 9.35l6.7-.55z" opacity="0.85" />
        </svg>
        {xp.toLocaleString()}
        <span className="hud-label">XP</span>
      </span>
    </div>
  );
}

/** Rank movement. Only rendered when we actually know it.
 *
 * The references show up/down arrows on every row. We do not store rank
 * history, so inventing an arrow would be inventing data -- `delta` is
 * optional and a row with no known movement renders a neutral dash. */
export function RankMove({ delta }: { delta?: number }) {
  if (delta === undefined || delta === 0) {
    return (
      <span className="lb-move lb-move-same" role="img" aria-label="no change">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <rect x="5" y="11" width="14" height="2.4" rx="1.2" />
        </svg>
      </span>
    );
  }
  const up = delta > 0;
  return (
    <span
      className={`lb-move ${up ? "lb-move-up" : "lb-move-down"}`}
      role="img"
      aria-label={`${up ? "up" : "down"} ${Math.abs(delta)}`}
    >
      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d={up ? "M12 5l7 9H5z" : "M12 19l-7-9h14z"} />
      </svg>
    </span>
  );
}

export function ArcadeRoute() {
  const [data, setData] = useState<ArcadeDashboard>();
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Loading your desk…");
  const [peerFilter, setPeerFilter] = useState("");
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const load = useCallback(async () => {
    try {
      const next = await api.getArcade();
      setData(next);
      setStatus("");
    } catch (err) {
      setError(userMessage(err));
      setStatus("");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  // Keep the desk current. Without this the peer-request badge only ever
  // reflected the state at page load, so a laptop left on the dashboard
  // never noticed that someone had recorded.
  usePolling(load, 8000);

  const pendingCount = data?.invitations.length ?? 0;
  const peers = (data?.peers ?? []).filter((p) =>
    p.display_name.toLowerCase().includes(peerFilter.trim().toLowerCase()),
  );

  // Real total across decks -- the field is the corpus, not confetti.
  const verifiedTotal = (data?.decks ?? []).reduce(
    (sum, deck) => sum + deck.verified_contributions,
    0,
  );

  return (
    <div className="desk">
      {data && <BubbleField count={verifiedTotal} />}
      <a className="skip-link" href="#desk-main">
        Skip to dashboard
      </a>

      {/* --- left menu ------------------------------------------------ */}
      <nav className="desk-nav" aria-label="Main">
        <p className="desk-brand">
          <span className="desk-brand-mark" aria-hidden="true" />
          AMAZWI
        </p>

        <p className="desk-nav-heading" id="nav-desk">
          My desk
        </p>
        <ul aria-labelledby="nav-desk">
          {NAV_PRIMARY.map((item) => (
            <li key={item.to}>
              <Link
                to={item.to}
                className={pathname === item.to ? "is-active" : undefined}
                aria-current={pathname === item.to ? "page" : undefined}
              >
                <span aria-hidden="true">{item.icon}</span>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>

        <p className="desk-nav-heading" id="nav-play">
          Play
        </p>
        <ul aria-labelledby="nav-play">
          <li>
            <Link
              to="/consent"
              className={pathname === "/consent" ? "is-active" : undefined}
              aria-current={pathname === "/consent" ? "page" : undefined}
            >
              <span aria-hidden="true">●</span>
              Record a card
            </Link>
          </li>
          <li>
            <Link to="/verify" className={`desk-nav-badged${pathname === "/verify" ? " is-active" : ""}`} aria-current={pathname === "/verify" ? "page" : undefined}>
              <span aria-hidden="true">◐</span>
              Peer requests
              {pendingCount > 0 && (
                <span className="desk-badge">
                  {pendingCount}
                  <span className="visually-hidden"> waiting for you</span>
                </span>
              )}
            </Link>
          </li>
        </ul>

        {/* The reference puts a "GO PRO" upsell here. There is no paid
            tier, so this slot carries the one fact a contributor most
            needs and cannot get anywhere else on the screen. */}
        <div className="desk-note">
          <p className="desk-note-title">Peer truth</p>
          <p>
            Two people must independently understand you before a clip counts.
            When they disagree, nobody is paid.
          </p>
        </div>
      </nav>

      {/* --- main ------------------------------------------------------ */}
      <main className="desk-main" id="desk-main" aria-labelledby="desk-title">
        <div aria-live="polite" aria-atomic="true" className="visually-hidden">
          {status}
        </div>
        {error && (
          <p role="alert" className="desk-error">
            {error}
          </p>
        )}
        {status && <p className="desk-loading">{status}</p>}

        {data && (
          <>
            <section className="desk-hero">
              <div className="desk-hero-copy">
                <p className="eyebrow">Today&rsquo;s voice mission</p>
                <h1 id="desk-title">Speak, be understood, earn.</h1>
                <p className="serif">
                  Describe the word without saying it. Two peers decide.
                </p>
                <CurrencyHud
                  earnedCents={data.earned_cents}
                  xp={data.progression.xp}
                />
                <div className="desk-hero-actions">
                  <button
                    type="button"
                    className="btn-primary"
                    onClick={() => navigate("/consent")}
                  >
                    Start speaking
                  </button>
                  <button
                    type="button"
                    className="btn-ghost"
                    onClick={() => navigate("/impact")}
                  >
                    View impact
                  </button>
                </div>
              </div>
              {/* The signature device, given a face. `understood` when
                  the speaker's last clips landed, so the mascot reflects
                  real state rather than smiling unconditionally. */}
              <Mascot
                size={132}
                mood={data.outcomes.understood > 0 ? "understood" : "idle"}
                className="desk-hero-mascot"
              />
            </section>

            {/* --- overview strip ------------------------------------- */}
            <h2 className="desk-section-title">Overview</h2>
            <div className="desk-overview">
              <article className="panel panel-profile rise-in">
                <div className="avatar avatar-lg" aria-hidden="true">
                  {initials(data.display_name)}
                </div>
                <p className="panel-name">{data.display_name}</p>
                <p className="panel-sub">
                  Level {data.progression.level} · {data.progression.tier}
                </p>
                <TierStars tier={data.progression.tier} />
                <div
                  className="xp-bar"
                  role="progressbar"
                  aria-valuemin={0}
                  aria-valuemax={data.progression.xp_for_next_level}
                  aria-valuenow={data.progression.xp_into_level}
                  aria-label={`Experience toward level ${data.progression.level + 1}`}
                >
                  <span style={{ width: `${data.progression.percent_into_level}%` }} />
                </div>
                <p className="panel-meta">
                  {data.progression.xp_into_level} / {data.progression.xp_for_next_level} XP
                  toward level {data.progression.level + 1}
                </p>
              </article>

              <article className="panel panel-earnings rise-in" style={{ "--rise-delay": "70ms" } as React.CSSProperties}>
                <p className="eyebrow">Credited to you</p>
                <p className="money">{formatRand(data.earned_cents)}</p>
                {/* Never "balance", never "paid" -- this is ledger credit. */}
                <p className="panel-meta">
                  Credited in the reward ledger. Cash-out is a separate,
                  reviewed step.
                </p>
                <dl className="panel-stats">
                  <div>
                    <dt>Clips verified</dt>
                    <dd>{data.progression.verified_contributions}</dd>
                  </div>
                  <div>
                    <dt>Peers helped</dt>
                    <dd>{data.progression.completed_verifications}</dd>
                  </div>
                </dl>
              </article>

              {/* The reference's radar slot, carrying real outcomes. */}
              <article className="panel panel-outcomes rise-in" style={{ "--rise-delay": "140ms" } as React.CSSProperties}>
                <p className="eyebrow">Your clips</p>
                {data.outcomes.total === 0 ? (
                  <p className="panel-empty">
                    No clips yet. Your first recording appears here.
                  </p>
                ) : (
                  <OutcomeBars outcomes={data.outcomes} />
                )}
              </article>
            </div>

            {/* --- decks ---------------------------------------------- */}
            <h2 className="desk-section-title">Voice decks</h2>
            <div className="deck-grid">
              {data.decks.map((deck) => (
                <article key={deck.language} className={`deck deck-${deck.language}`}>
                  <h3>{languageName(deck.language)}</h3>
                  <p className="deck-meta">
                    {deck.card_count} cards · {deck.contributors}{" "}
                    {deck.contributors === 1 ? "contributor" : "contributors"}
                  </p>
                  <p className="deck-verified">
                    {deck.verified_contributions} verified
                  </p>
                  <button
                    type="button"
                    className="btn-pill"
                    onClick={() => navigate("/consent")}
                  >
                    Play now
                    <span className="visually-hidden">
                      {" "}
                      in {languageName(deck.language)}
                    </span>
                  </button>
                </article>
              ))}
            </div>

            <div className="desk-columns">
              {/* --- leaderboard -------------------------------------- */}
              <section aria-labelledby="lb-title" className="panel">
                <h2 id="lb-title">
                  Leaderboard
                  {data.leaderboard_language && (
                    <span className="panel-tag">
                      {languageName(data.leaderboard_language)}
                    </span>
                  )}
                </h2>
                {data.leaderboard.length === 0 ? (
                  <p className="panel-empty">
                    No verified contributions in this language yet.
                  </p>
                ) : (
                  <Leaderboard rows={data.leaderboard} />
                )}
              </section>

              {/* --- quests ------------------------------------------- */}
              <section aria-labelledby="quest-title" className="panel">
                <h2 id="quest-title">Daily quest</h2>
                <ul className="quest-list">
                  {data.quests.map((quest) => (
                    <QuestItem key={quest.key} quest={quest} />
                  ))}
                </ul>
              </section>
            </div>
          </>
        )}
      </main>

      {/* --- right rail ------------------------------------------------ */}
      {data && (
        <aside className="desk-rail" aria-label="Requests and peers">
          <section aria-labelledby="inv-title">
            <h2 id="inv-title" className="rail-title">
              Peer requests
            </h2>
            {data.invitations.length === 0 ? (
              <p className="panel-empty">
                Nobody is waiting on you right now.
              </p>
            ) : (
              <ul className="invite-list">
                {data.invitations.map((invite) => (
                  <li key={invite.assignment_id} className="invite">
                    <div className="avatar" aria-hidden="true">
                      {initials(invite.speaker_name)}
                    </div>
                    <div className="invite-body">
                      <p className="invite-name">{invite.speaker_name}</p>
                      <p className="invite-sub">
                        wants you to listen · {languageName(invite.language)}
                      </p>
                      <div className="invite-actions">
                        <button
                          type="button"
                          className="btn-pill"
                          onClick={() =>
                            navigate(
                              `/verify?contributionId=${encodeURIComponent(
                                invite.contribution_id,
                              )}`,
                            )
                          }
                        >
                          Listen
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section aria-labelledby="peers-title">
            <h2 id="peers-title" className="rail-title">
              Your language cohort
            </h2>
            <label className="visually-hidden" htmlFor="peer-filter">
              Filter peers by name
            </label>
            <input
              id="peer-filter"
              type="search"
              className="rail-search"
              placeholder="Search peers"
              value={peerFilter}
              onChange={(event) => setPeerFilter(event.target.value)}
            />
            {peers.length === 0 ? (
              <p className="panel-empty">
                {data.peers.length === 0
                  ? "No qualified peers in your language yet."
                  : "No peer matches that name."}
              </p>
            ) : (
              <ul className="peer-list">
                {peers.map((peer) => (
                  <li key={peer.user_id} className="peer">
                    <div className="avatar" aria-hidden="true">
                      {initials(peer.display_name)}
                    </div>
                    <div>
                      <p className="peer-name">{peer.display_name}</p>
                      <p className="peer-tier">
                        {peer.tier} · {languageName(peer.language)}
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </aside>
      )}

      {/* Mobile only -- above 820px the left rail already does this job
          and two navigations would compete for the same intent. */}
      <TabBar pendingCount={pendingCount} />
    </div>
  );
}

/** Real outcome split. Exported so a test can render it in isolation. */
export function OutcomeBars({
  outcomes,
}: {
  outcomes: ArcadeDashboard["outcomes"];
}) {
  const rows = [
    { label: "Understood", value: outcomes.understood, tone: "ok" },
    { label: "Not understood", value: outcomes.not_understood, tone: "miss" },
    { label: "Waiting on peers", value: outcomes.awaiting_peers, tone: "wait" },
    { label: "Closed", value: outcomes.closed, tone: "closed" },
  ].filter((row) => row.value > 0);

  return (
    <ul className="outcome-list">
      {rows.map((row) => (
        <li key={row.label}>
          <span className="outcome-label">{row.label}</span>
          <span className={`outcome-bar outcome-${row.tone}`}>
            <span
              style={{
                width: `${Math.round((100 * row.value) / Math.max(1, outcomes.total))}%`,
              }}
            />
          </span>
          <span className="outcome-value">{row.value}</span>
        </li>
      ))}
    </ul>
  );
}

export function Leaderboard({ rows }: { rows: LeaderboardRow[] }) {
  const podium = rows.slice(0, 3);
  const rest = rows.slice(3);
  // Visual podium order is 2nd, 1st, 3rd. The DOM keeps rank order so a
  // screen reader and the keyboard hear first place first; CSS `order`
  // does the rearranging.
  return (
    <>
      {podium.length > 0 && (
        <ol className="podium">
          {podium.map((row) => (
            <li
              key={row.user_id}
              className={`podium-slot podium-${row.rank}${
                row.is_current_user ? " is-you" : ""
              }`}
            >
              {row.rank === 1 && (
                <svg className="podium-crown" width="20" height="14" viewBox="0 0 24 16" fill="currentColor" aria-hidden="true">
                  <path d="M2 14h20l-1.6-9.4-5 3.6L12 1.4 8.6 8.2l-5-3.6z" />
                </svg>
              )}
              <div className="avatar avatar-lg" aria-hidden="true">
                {initials(row.display_name)}
              </div>
              <p className="podium-rank">#{row.rank}</p>
              <p className="podium-name">{row.display_name}</p>
              <p className="podium-score">{row.verified_contributions} verified</p>
              {row.is_current_user && <p className="podium-you">You</p>}
              {/* The bar IS the ranking -- equal flat cards threw away
                  the one thing a podium is for. */}
              <div className="podium-bar">{row.rank}</div>
            </li>
          ))}
        </ol>
      )}
      {rest.length > 0 && (
        <ol className="lb-list" start={4}>
          {rest.map((row) => (
            <li key={row.user_id} className={row.is_current_user ? "is-you" : ""}>
              <span className="lb-rank">{row.rank}</span>
              <div className="avatar" aria-hidden="true">
                {initials(row.display_name)}
              </div>
              <span className="lb-name">
                {row.display_name}
                {row.is_current_user && <span className="lb-you"> (you)</span>}
              </span>
              <span className="lb-tier"><TierStars tier={row.tier} /></span>
              <RankMove />
              <span className="lb-score">{row.verified_contributions}</span>
            </li>
          ))}
        </ol>
      )}
    </>
  );
}

export function QuestItem({ quest }: { quest: QuestRow }) {
  const percent = Math.round((100 * quest.progress) / quest.target);
  return (
    <li className={`quest${quest.complete ? " is-complete" : ""}`} style={{ position: "relative" }}>
      {quest.complete && <Burst />}
      <div className="quest-head">
        <p className="quest-label">{quest.label}</p>
        <p className="quest-xp">+{quest.reward_xp} XP</p>
      </div>
      <p className="quest-detail">{quest.detail}</p>
      <div
        className="quest-bar"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={quest.target}
        aria-valuenow={quest.progress}
        aria-label={quest.label}
      >
        <span style={{ width: `${percent}%` }} />
      </div>
      <p className="quest-progress">
        {quest.progress} / {quest.target}
        {quest.complete ? " · complete" : " done today"}
      </p>
    </li>
  );
}
