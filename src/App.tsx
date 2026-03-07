import React, { useState } from "react";
import Login from "./components/Login";
import Workspace from "./components/Workspace";
import SearchPapers from "./components/SearchPapers";
import Chatbot from "./components/Chatbot";

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [workspaceId, setWorkspaceId] = useState<number | null>(null);
  const [workspaceName, setWorkspaceName] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"papers" | "chat">("papers");

  // Called after successful login
  const handleLogin = (t: string) => {
    localStorage.setItem("token", t);
    setToken(t);
  };

  // Clear session and return to login
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setWorkspaceId(null);
    setWorkspaceName("");
  };

  // Show login screen if not authenticated
  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", background: "#0d1117" }}>

      {/* ── Top Bar ─────────────────────────────────────────────────────── */}
      <header style={{
        height: 52, display: "flex", alignItems: "center",
        justifyContent: "space-between", padding: "0 20px",
        background: "#111827", borderBottom: "1px solid rgba(255,255,255,0.07)",
        flexShrink: 0
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{
            width: 8, height: 8, borderRadius: "50%",
            background: "#2f81f7", boxShadow: "0 0 8px #2f81f7"
          }} />
          <span style={{
            fontFamily: "Georgia, serif", fontSize: 18,
            fontWeight: 700, letterSpacing: -0.5, color: "#e6edf3"
          }}>
            ResearchHub <span style={{ color: "#2f81f7" }}>AI</span>
          </span>
        </div>

        {/* Right side */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {/* Live badge */}
          <div style={{
            fontSize: 11, fontWeight: 600, padding: "3px 10px",
            borderRadius: 99, background: "rgba(63,185,80,0.12)",
            color: "#3fb950", border: "1px solid rgba(63,185,80,0.25)",
            display: "flex", alignItems: "center", gap: 5
          }}>
            <div style={{
              width: 5, height: 5, borderRadius: "50%",
              background: "#3fb950", animation: "pulse 2s infinite"
            }} />
            Backend connected
          </div>

          {/* Tab switcher */}
          <div style={{ display: "flex", gap: 4 }}>
            {(["papers", "chat"] as const).map(t => (
              <button key={t} onClick={() => setActiveTab(t)} style={{
                background: activeTab === t ? "rgba(47,129,247,0.12)" : "none",
                border: activeTab === t ? "1px solid rgba(47,129,247,0.25)" : "1px solid transparent",
                color: activeTab === t ? "#2f81f7" : "#8b949e",
                borderRadius: 8, padding: "5px 14px",
                fontSize: 12, fontWeight: 600, cursor: "pointer",
                fontFamily: "inherit", transition: "all 0.15s"
              }}>
                {t === "papers" ? "📄 Papers" : "🤖 AI Chat"}
              </button>
            ))}
          </div>

          {/* Logout */}
          <button onClick={handleLogout} style={{
            background: "none", border: "1px solid rgba(255,255,255,0.08)",
            color: "#8b949e", borderRadius: 8, padding: "5px 12px",
            fontSize: 12, cursor: "pointer", fontFamily: "inherit",
            transition: "all 0.15s"
          }}
            onMouseEnter={e => { (e.target as HTMLButtonElement).style.color = "#f85149"; }}
            onMouseLeave={e => { (e.target as HTMLButtonElement).style.color = "#8b949e"; }}
          >
            Sign out
          </button>
        </div>
      </header>

      {/* ── Main Layout ─────────────────────────────────────────────────── */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>

        {/* Sidebar */}
        <div style={{
          width: 220, flexShrink: 0,
          background: "#111827", borderRight: "1px solid rgba(255,255,255,0.07)",
          overflow: "hidden"
        }}>
          <Workspace
            onSelect={(id, name) => {
              setWorkspaceId(id);
              setWorkspaceName(name);
            }}
            selectedId={workspaceId}
          />
        </div>

        {/* Content */}
        <div style={{ flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" }}>
          {activeTab === "papers" && (
            <SearchPapers
              workspaceId={workspaceId}
              workspaceName={workspaceName}
            />
          )}
          {activeTab === "chat" && (
            <Chatbot
              workspaceId={workspaceId}
              workspaceName={workspaceName}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default App