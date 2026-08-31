import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState<string>("checking...");

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then((d) => setStatus(`${d.status} (${d.provider_mode})`))
      .catch(() => setStatus("backend unreachable"));
  }, []);

  return (
    <main>
      <h1>starter</h1>
      <p>backend: {status}</p>
    </main>
  );
}
