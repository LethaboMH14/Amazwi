/**
 * Mobile bottom tab bar, with a raised centre action.
 *
 * Mobile only. On desktop the left rail already does this job, and
 * shipping both would be two navigations competing for the same intent.
 *
 * The raised centre is Record. That is not a style copy of the
 * references -- it is the correct use of the pattern here. Recording is
 * the one action the whole product exists to collect, and the centre
 * slot is the only spot on a phone every thumb reaches without a
 * stretch.
 *
 * Accessibility carried, not dropped for looks:
 *   - a real <nav> with a label, real <Link>s, aria-current on the
 *     active tab
 *   - 44px minimum targets, met by padding so labels can grow at 200%
 *     zoom without clipping
 *   - the icon is decorative; every tab carries a visible text label,
 *     so nobody has to decode a glyph
 *   - safe-area inset padding, so the last row is not sitting under the
 *     iPhone home indicator
 */
import { Link, useLocation } from "react-router-dom";
import "./tabbar.css";

type Tab = {
  to: string;
  label: string;
  icon: JSX.Element;
  center?: boolean;
  badge?: number;
};

const ICON = {
  home: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 10.5L12 3l9 7.5" />
      <path d="M5.5 9.5V20h13V9.5" />
    </svg>
  ),
  gift: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="9" width="18" height="12" rx="2" />
      <path d="M3 13h18M12 9v12" />
      <path d="M12 9C10 9 7.5 8.4 7.5 6.4A2.4 2.4 0 0 1 12 5.6a2.4 2.4 0 0 1 4.5.8C16.5 8.4 14 9 12 9z" />
    </svg>
  ),
  mic: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3z" />
      <path d="M5 11a7 7 0 0 0 14 0M12 18v3" />
    </svg>
  ),
  // Headphones, not an ear: the ear outline rendered as an unreadable
  // squiggle at 22px. Caught by looking at it, not by reading the path.
  ear: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 14v-2a8 8 0 0 1 16 0v2" />
      <rect x="2.5" y="13.5" width="4.5" height="7" rx="2.25" />
      <rect x="17" y="13.5" width="4.5" height="7" rx="2.25" />
    </svg>
  ),
  map: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 4L3.5 6.4v13L9 17l6 2.6 5.5-2.4v-13L15 6.4z" />
      <path d="M9 4v13M15 6.6v13" />
    </svg>
  ),
};

export function TabBar({ pendingCount = 0 }: { pendingCount?: number }) {
  const { pathname } = useLocation();

  const tabs: Tab[] = [
    { to: "/dashboard", label: "Home", icon: ICON.home },
    { to: "/rewards", label: "Rewards", icon: ICON.gift },
    { to: "/consent", label: "Record", icon: ICON.mic, center: true },
    { to: "/verify", label: "Listen", icon: ICON.ear, badge: pendingCount },
    { to: "/impact", label: "Impact", icon: ICON.map },
  ];

  return (
    <nav className="tabbar" aria-label="Primary">
      <ul>
        {tabs.map((tab) => {
          const active = pathname === tab.to;
          return (
            <li key={tab.to} className={tab.center ? "tab-center-slot" : undefined}>
              <Link
                to={tab.to}
                className={`tab${tab.center ? " tab-center" : ""}${active ? " is-active" : ""}`}
                aria-current={active ? "page" : undefined}
              >
                <span className="tab-icon" aria-hidden="true">
                  {tab.icon}
                  {!!tab.badge && tab.badge > 0 && (
                    <span className="tab-badge">{tab.badge > 9 ? "9+" : tab.badge}</span>
                  )}
                </span>
                <span className="tab-label">{tab.label}</span>
                {!!tab.badge && tab.badge > 0 && (
                  <span className="visually-hidden">
                    , {tab.badge} waiting for you
                  </span>
                )}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
