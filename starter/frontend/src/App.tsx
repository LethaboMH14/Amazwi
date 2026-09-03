import { BrowserRouter, Routes, Route } from "react-router-dom";
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
      <Routes>
        <Route path="/" element={<HomeRoute />} />
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
