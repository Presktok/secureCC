import "./App.css";
import { useState } from "react";
import AuthPage from "./components/AuthPage";
import CodeEditor from "./components/CodeEditor";
import GetStartedPage from "./components/GetStartedPage";

function App() {
  const [user, setUser] = useState(() => {
    try {
      return window.localStorage.getItem("securecc_session") || "";
    } catch {
      return "";
    }
  });
  const [showAuth, setShowAuth] = useState(Boolean(user));
  const [theme, setTheme] = useState(() => {
    try {
      return window.localStorage.getItem("securecc_theme") || "midnight";
    } catch {
      return "midnight";
    }
  });

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    try {
      window.localStorage.setItem("securecc_theme", newTheme);
    } catch {
    }
  };

  return (
    <div className={`App theme-${theme}`}>
      {user ? (
        <CodeEditor
          user={user}
          onLogout={() => {
            setUser("");
            setShowAuth(false);
          }}
          currentTheme={theme}
          onThemeChange={handleThemeChange}
        />
      ) : showAuth ? (
        <AuthPage onAuthSuccess={setUser} theme={theme} onThemeChange={handleThemeChange} />
      ) : (
        <GetStartedPage onContinue={() => setShowAuth(true)} theme={theme} onThemeChange={handleThemeChange} />
      )}
    </div>
  );
}

export default App;
