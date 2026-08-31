import { useEffect, useState } from "react";
import { createHostBridge } from "./hostBridge";

export default function App() {
  const [backendStatus, setBackendStatus] = useState<string>("checking...");
  const [hostMode, setHostMode] = useState<string>("checking...");

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then((d) => setBackendStatus(`${d.status} (${d.provider_mode})`))
      .catch(() => setBackendStatus("backend unreachable"));
  }, []);

  useEffect(() => {
    const bridge = createHostBridge();
    setHostMode(bridge.mode);
    bridge.start();
    return () => bridge.stop();
  }, []);

  return (
    <main>
      <h1>starter</h1>
      <p>backend: {backendStatus}</p>
      <p>host bridge: {hostMode}</p>
    </main>
  );
}
