import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomeRoute } from "./HomeRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomeRoute />} />
      </Routes>
    </BrowserRouter>
  );
}
