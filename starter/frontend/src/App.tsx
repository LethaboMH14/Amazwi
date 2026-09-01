import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomeRoute } from "./HomeRoute";
import { ConsentRoute } from "./features/consent/ConsentRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeRoute />} />
        <Route path="/consent" element={<ConsentRoute />} />
      </Routes>
    </BrowserRouter>
  );
}
