import { useState } from "react";
import ThemeSwitcher from "./ThemeSwitcher";

const USERS_KEY = "securecc_users";
const SESSION_KEY = "securecc_session";

function loadUsers() {
  try {
    const raw = window.localStorage.getItem(USERS_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function saveUsers(users) {
  window.localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

export default function AuthPage({ onAuthSuccess, theme, onThemeChange }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const resetFeedback = () => {
    setMessage("");
    setError("");
  };

  const handleSignup = () => {
    resetFeedback();
    if (!username.trim() || !password) {
      setError("Username and password are required.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const users = loadUsers();
    if (users[username]) {
      setError("Username already exists.");
      return;
    }

    users[username] = password;
    saveUsers(users);
    setMessage("Signup successful. Please login.");
    setMode("login");
    setPassword("");
    setConfirmPassword("");
  };

  const handleLogin = () => {
    resetFeedback();
    const users = loadUsers();
    if (!users[username] || users[username] !== password) {
      setError("Invalid username or password.");
      return;
    }

    window.localStorage.setItem(SESSION_KEY, username);
    onAuthSuccess(username);
  };

  return (
    <div className="auth-screen">
      <div className="auth-card neon-panel">
        <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'center' }}>
          <ThemeSwitcher currentTheme={theme} onThemeChange={onThemeChange} />
        </div>
        <h1>SecureCC</h1>
        <p className="auth-subtitle">Login or create an account to continue</p>

        <div className="auth-tabs">
          <button
            type="button"
            className={mode === "login" ? "auth-tab auth-tab-active" : "auth-tab"}
            onClick={() => {
              setMode("login");
              resetFeedback();
            }}
          >
            Login
          </button>
          <button
            type="button"
            className={mode === "signup" ? "auth-tab auth-tab-active" : "auth-tab"}
            onClick={() => {
              setMode("signup");
              resetFeedback();
            }}
          >
            Sign Up
          </button>
        </div>

        <div className="auth-form">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
          />

          {mode === "signup" ? (
            <>
              <label htmlFor="confirm-password">Confirm Password</label>
              <input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter password"
              />
            </>
          ) : null}

          {error ? <div className="auth-error">{error}</div> : null}
          {message ? <div className="auth-message">{message}</div> : null}

          <button
            type="button"
            className="auth-submit"
            onClick={mode === "signup" ? handleSignup : handleLogin}
          >
            {mode === "signup" ? "Create Account" : "Login"}
          </button>
        </div>
      </div>
    </div>
  );
}
