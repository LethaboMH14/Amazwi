import { useEffect } from "react";
import { useLocation } from "react-router-dom";

/**
 * Reset scroll on navigation.
 *
 * A single-page app keeps the scroll offset across route changes, so
 * moving from a scrolled dashboard to the record screen landed you
 * halfway down a screen whose top carried the whole point -- the word you
 * are meant to describe. Nothing was broken; it just looked like it.
 *
 * `instant` rather than smooth: an animated jump on every navigation is
 * motion nobody asked for, and it fights `prefers-reduced-motion`.
 */
export function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: "instant" as ScrollBehavior });
  }, [pathname]);
  return null;
}
