import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomeRoute } from "./HomeRoute";
import { ConsentRoute } from "./features/consent/ConsentRoute";
import { RecordingRoute } from "./features/recording/RecordingRoute";
import { VerificationRoute } from "./features/verification/VerificationRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeRoute />} />
        <Route path="/consent" element={<ConsentRoute />} />
        <Route path="/record/:contributionId" element={<RecordingRoute />} />
        <Route path="/verify" element={<VerificationRoute />} />
      </Routes>
    </BrowserRouter>
  );
}
