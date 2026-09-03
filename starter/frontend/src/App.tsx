import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ScrollToTop } from "./ScrollToTop";
import { LiveWatch } from "./features/arcade/LiveWatch";
import { HomeRoute } from "./HomeRoute";
import { ConsentRoute } from "./features/consent/ConsentRoute";
import { RecordingRoute } from "./features/recording/RecordingRoute";
import { VerificationRoute } from "./features/verification/VerificationRoute";
import { ResultRoute } from "./features/result/ResultRoute";
import { ImpactRoute } from "./features/impact/ImpactRoute";
import { OpsRoute } from "./features/ops/OpsRoute";
import { ArcadeRoute } from "./features/arcade/ArcadeRoute";
import { RewardsRoute } from "./features/rewards/RewardsRoute";
import { AssistantWidget } from "./AssistantWidget";

export default function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      {/* App-wide, so a verifier waiting on any screen is told a
          recording arrived without reloading the page. */}
      <LiveWatch />
      <Routes>
        {/* The desk is the product; the old marketing home is not what a
            device should land on. Every demo device opens a bare origin
            with no path, and landing on a screen with one button was the
            "why is it loading this" moment. Kept at /welcome so the Gate A
            narrative screen is not lost. */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/welcome" element={<HomeRoute />} />
        <Route path="/consent" element={<ConsentRoute />} />
        <Route path="/record" element={<RecordingRoute />} />
        <Route path="/verify" element={<VerificationRoute />} />
        <Route path="/result/:contributionId" element={<ResultRoute />} />
        <Route path="/impact" element={<ImpactRoute />} />
        <Route path="/ops" element={<OpsRoute />} />
        <Route path="/dashboard" element={<ArcadeRoute />} />
        <Route path="/rewards" element={<RewardsRoute />} />
      </Routes>
      <AssistantWidget />
    </BrowserRouter>
  );
}
