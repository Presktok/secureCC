import React from 'react';

const themes = [
  { id: 'midnight', name: 'Midnight', color: '#8b5cf6' },
  { id: 'slate', name: 'Slate', color: '#64748b' },
  { id: 'snow', name: 'Snow', color: '#ffffff' },
];

export default function ThemeSwitcher({ currentTheme, onThemeChange }) {
  return (
    <div className="theme-switcher">
      <div className="theme-options">
        {themes.map((theme) => (
          <button
            key={theme.id}
            className={`theme-option ${currentTheme === theme.id ? 'active' : ''}`}
            onClick={() => onThemeChange(theme.id)}
            title={`Switch to ${theme.name} theme`}
          >
            <span 
              className="theme-preview-dot" 
              style={{ backgroundColor: theme.color }}
            />
            <span className="theme-name">{theme.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
