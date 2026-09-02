/**
 * My Rewards -- the redemption screen.
 *
 * Layout follows the mobile fintech reference frame (360x804): a bold
 * heading, a gradient balance card with a pill CTA and artwork bleeding
 * off the right edge, a stack of bordered reward cards each with a cost
 * cluster and a "view details" action, and a bottom tab bar.
 *
 * Three things from that reference are deliberately NOT reproduced,
 * because AMAZWI would be lying if it showed them:
 *
 *   1. **No merchant offers.** The reference lists a retailer discount.
 *      AMAZWI has no retail partners. Every item here maps to a product
 *      MTN MoMo genuinely operates -- airtime, data, wallet cash-out --
 *      and the backend has a test that fails if a brand name appears.
 *   2. **No prize draw, and no scarcity badge.** The reference's green
 *      "Hurry up only 53 slots left!" pill is a countdown against an
 *      inventory that, here, does not exist. That badge slot is kept --
 *      same position, same visual weight -- and carries the honest
 *      availability state instead. Same pixel, opposite intent.
 *   3. **No points balance.** The reference shows "12 points". The
 *      AMAZWI ledger is denominated in rand, so this screen shows rand.
 *      A parallel points currency would be a second source of truth for
 *      money.
 *
 * The redeem action is driven entirely by `availability`, which the
 * server computes from the live provider mode. Under the DemoProvider
 * every row comes back PROVIDER_NOT_CONNECTED and no redeem button is
 * rendered at all -- not a disabled one, not a "coming soon" one that
 * still looks tappable.
 */
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, userMessage } from "../../api/client";
import type { CatalogueRow, RewardAvailability, Rewards } from "../../api/contracts";
import { formatRand } from "../arcade/ArcadeRoute";
import "./rewards.css";

/** Copy for each availability state. Never implies a live provider. */
export function availabilityLabel(
  availability: RewardAvailability,
  shortfallCents: number,
): string {
  switch (availability) {
    case "REDEEMABLE":
      return "Ready to redeem";
    case "INSUFFICIENT_CREDIT":
      return `${formatRand(shortfallCents)} more to unlock`;
    case "PROVIDER_NOT_CONNECTED":
      return "Not redeemable in demo mode";
  }
}

export function RewardsRoute() {
  const [data, setData] = useState<Rewards>();
  const [error, setError] = useState("");
  const [status, setStatus] = useState("Loading your rewards…");
  const navigate = useNavigate();

  const load = useCallback(async () => {
    try {
      setData(await api.getRewards());
      setStatus("");
    } catch (err) {
      setError(userMessage(err));
      setStatus("");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <main className="rewards" aria-labelledby="rewards-title">
      <div aria-live="polite" aria-atomic="true" className="visually-hidden">
        {status}
      </div>

      <h1 id="rewards-title">My rewards</h1>

      {error && (
        <p role="alert" className="rewards-error">
          {error}
        </p>
      )}
      {status && <p className="rewards-loading">{status}</p>}

      {data && (
        <>
          {/* Balance card. The reference's "12 points" becomes the real
              ledger figure, and the sub-line refuses the word balance. */}
          <section className="balance-card" aria-labelledby="balance-title">
            <div className="balance-art" aria-hidden="true">
              <span className="coin coin-1" />
              <span className="coin coin-2" />
              <span className="coin coin-3" />
              <span className="coin coin-4" />
              <span className="coin coin-5" />
            </div>
            <div className="balance-body">
              <h2 id="balance-title" className="visually-hidden">
                Your credited rewards
              </h2>
              <p className="balance-figure">
                <span className="money">{formatRand(data.balance_cents)}</span>{" "}
                <span className="balance-unit">credited</span>
              </p>
              <p className="balance-note">
                Credited in the reward ledger. Cash-out is a separate,
                reviewed step.
              </p>
              <button
                type="button"
                className="btn-earn"
                onClick={() => navigate("/consent")}
              >
                <span aria-hidden="true" className="btn-earn-dot" />
                Earn more
              </button>
            </div>
          </section>

          {/* The provider truth, stated once and plainly, above the list
              rather than buried in each card. */}
          {!data.provider_connected && (
            <p className="provider-note" role="note">
              <strong>Demo provider.</strong> Nothing below can be redeemed
              yet — no live MoMo provider is connected to this build.
            </p>
          )}

          <ul className="reward-list">
            {data.items.map((item) => (
              <RewardCard key={item.key} item={item} />
            ))}
          </ul>

          {data.thresholds_are_proposed && (
            <p className="rewards-footnote">
              Redemption amounts are proposed, not final — they are a money
              decision still under review.
            </p>
          )}
        </>
      )}
    </main>
  );
}

export function RewardCard({ item }: { item: CatalogueRow }) {
  const [open, setOpen] = useState(false);
  const detailsId = `reward-details-${item.key}`;

  return (
    <li className="reward-card">
      <div className="reward-head">
        <div className="reward-copy">
          <h2>{item.title}</h2>
          <p>{item.description}</p>
        </div>
        {/* The reference's coin-stack + number cost cluster. */}
        <div className="reward-cost">
          <span className="reward-coins" aria-hidden="true">
            <span /> <span /> <span />
          </span>
          <span className="reward-price">{formatRand(item.threshold_cents)}</span>
        </div>
      </div>

      <div className="reward-actions">
        {/* The reference's scarcity badge slot, carrying the honest
            availability state instead of a fake countdown. */}
        <span className={`reward-state state-${item.availability.toLowerCase()}`}>
          {availabilityLabel(item.availability, item.shortfall_cents)}
        </span>

        <div className="reward-buttons">
          {/* Only ever rendered when the server says it is redeemable --
              never a disabled button that still reads as an offer. */}
          {item.availability === "REDEEMABLE" && (
            <button type="button" className="btn-redeem">
              Redeem
            </button>
          )}
          <button
            type="button"
            className="btn-details"
            aria-expanded={open}
            aria-controls={detailsId}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? "hide details" : "view details"}
          </button>
        </div>
      </div>

      {open && (
        <dl className="reward-details" id={detailsId}>
          <div>
            <dt>MoMo product</dt>
            <dd>{item.momo_product}</dd>
          </div>
          <div>
            <dt>Unlocks at</dt>
            <dd>{formatRand(item.threshold_cents)} credited</dd>
          </div>
        </dl>
      )}
    </li>
  );
}
