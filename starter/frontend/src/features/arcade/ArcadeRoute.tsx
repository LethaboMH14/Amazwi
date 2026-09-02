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
import { Link, useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { ArcadeDashboard, LeaderboardRow, QuestRow } from "../../api/contracts";
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

export function ArcadeRoute() {
  const [data, setData] = useState<ArcadeDashboard>();
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Loading your desk…");
  const [peerFilter, setPeerFilter] = useState("");
  const navigate = useNavigate();

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

  const pendingCount = data?.invitations.length ?? 0;
  const peers = (data?.peers ?? []).filter((p) =>
    p.display_name.toLowerCase().includes(peerFilter.trim().toLowerCase()),
  );

  return (
    <div className="desk">
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
              <Link to={item.to}>
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
            <Link to="/consent">
              <span aria-hidden="true">●</span>
              Record a card
            </Link>
          </li>
          <li>
            <Link to="/verify" className="desk-nav-badged">
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
              <div className="desk-hero-figure" aria-hidden="true">
                <span className="listener listener-a" />
                <span className="listener listener-b" />
              </div>
            </section>

            {/* --- overview strip ------------------------------------- */}
            <h2 className="desk-section-title">Overview</h2>
            <div className="desk-overview">
              <article className="panel panel-profile">
                <div className="avatar avatar-lg" aria-hidden="true">
                  {initials(data.display_name)}
                </div>
                <p className="panel-name">{data.display_name}</p>
                <p className="panel-sub">
                  Level {data.progression.level} · {data.progression.tier}
                </p>
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

              <article className="panel panel-earnings">
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
              <article className="panel panel-outcomes">
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
              <div className="avatar avatar-lg" aria-hidden="true">
                {initials(row.display_name)}
              </div>
              <p className="podium-rank">#{row.rank}</p>
              <p className="podium-name">{row.display_name}</p>
              <p className="podium-score">{row.verified_contributions} verified</p>
              {row.is_current_user && <p className="podium-you">You</p>}
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
              <span className="lb-tier">{row.tier}</span>
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
    <li className={`quest${quest.complete ? " is-complete" : ""}`}>
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
