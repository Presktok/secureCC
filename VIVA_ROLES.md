# SecureCC - Viva Project Roles

This document outlines the division of work for the **SecureCC** frontend for the purpose of the viva/presentation.

---

## Person 1: Core System Architect & Logic
**Focus**: Application infrastructure, security analysis integration, and core editor functionality.

### Key Contributions:
*   **`App.js` (Infrastructure)**: Designed the main application shell and component routing. Implemented global state management for theme switching.
*   **`CodeEditor.js` (Core Engine)**: Integrated the **Monaco Editor**. Developed the logic to communicate with the **FastAPI Backend**.
*   **API Synchronization**: Implemented real-time parsing of vulnerability results and mapped them to line-specific markers in the editor.

---

## Person 2: UI/UX Designer & Feature Specialist
**Focus**: Visual identity, user onboarding, authentication, and the multi-theme system.

### Key Contributions:
*   **`App.css` & `index.css` (Design System)**: Created a high-end **Glassmorphic UI** using advanced CSS filters. Developed the responsive grid system.
*   **`GetStartedPage.js` (User Onboarding)**: Designed the interactive landing page with custom CSS particle animations and scroll-triggered transitions.
*   **`AuthPage.js` (Secure Access)**: Built the Login and Signup interfaces with real-time field validation.
*   **`ThemeSwitcher.js` (Personalization)**: Implemented the multi-theme switching engine (Midnight, Slate, Snow, etc.) and integrated it into the main IDE workspace.

---

## Technical Stack Summary
- **Frontend**: React (v19), Monaco Editor, Vanilla CSS.
- **Backend**: FastAPI (Python), Static Analysis Engine (Lexer, Parser, Analyzer).
- **Styling**: Modern dark themes with HSL fine-tuning.
