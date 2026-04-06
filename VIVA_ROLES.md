# SecureCC - Viva Project Roles

This document outlines the division of work for the **SecureCC** frontend for the purpose of the viva/presentation. The project is divided into two primary roles: **Core System Architect** and **UI/UX & Feature Developer**.

---

## Person 1: Core System Architect & Logic
**Focus**: Application infrastructure, security analysis integration, and core editor functionality.

### Key Contributions:
*   **`App.js` (Infrastructure)**:
    *   Designed the main application shell and component routing.
    *   Implemented global state management for theme switching and page navigation.
*   **`CodeEditor.js` (Core Engine)**:
    *   Integrated the **Monaco Editor** for a professional coding experience.
    *   Developed the logic to communicate with the **FastAPI Backend**.
    *   Implemented real-time parsing of vulnerability results (buffer overflow, risky calls) and mapped them to line-specific markers in the editor.
*   **API Synchronization**:
    *   Ensured asynchronous handling of code analysis requests to maintain a smooth UI.

---

## Person 2: UI/UX Designer & Feature Specialist
**Focus**: Visual identity, user onboarding, authentication, and the multi-theme system.

### Key Contributions:
*   **`App.css` & `index.css` (Design System)**:
    *   Created a high-end **Glassmorphic UI** using advanced CSS filters and backdrops.
    *   Developed a responsive grid system that works across different screen sizes.
*   **`GetStartedPage.js` (User Onboarding)**:
    *   Designed the interactive landing page with custom CSS particle animations and scroll-triggered transitions.
    *   Implemented the "Threat Scan" mock visualization for product educational value.
*   **`AuthPage.js` (Secure Access)**:
    *   Built the Login and Signup interfaces with real-time field validation and state management.
*   **`ThemeSwitcher.js` (Personalization)**:
    *   Implemented the multi-theme switching engine (Midnight, Slate, Snow, etc.) and connected it to the global CSS variables.

---

## Summary of Tech Stack
*   **Frontend**: React.js (v19), Monaco Editor, Vanilla CSS.
*   **Backend Interface**: Axios/Fetch for REST API communication.
*   **Design**: Modern Dark Mode, Acrylic effects, and custom-tuned HSL color palettes.
