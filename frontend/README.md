# SecureCC - Security-Aware Compiler Dashboard (Frontend)

SecureCC is a professional-grade security-aware compiler framework with a modern terminal-inspired dashboard. It provides real-time C code analysis for common vulnerabilities like buffer overflows and risky function calls.

## Key Features

- **Real-time Code Analysis**: Instant feedback on security risks within the Monaco Editor.
- **Multi-Theme Support**: Choice of "Midnight", "Slate", and "Snow" themes for developer comfort.
- **Interactive UI**: High-end glassmorphic design with smooth transitions and particle animations.
- **Secure Onboarding**: Dedicated "Get Started" and "Authentication" workflows.

## Getting Started

### Prerequisites

- Node.js (v18+)
- npm

### Installation

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

### Running the App

Run the development server:
```bash
npm start
```
The application will be available at [http://localhost:3000](http://localhost:3000).

---

## Technical Division of Labor (Viva Overview)

For the purpose of development and presentation, the frontend work was divided between two core roles:

### 1. Core System Architect & Logic (Person 1)
- **Infrastructure**: App routing, state management, and component architecture (`App.js`, `index.js`).
- **Core Engine**: Monaco Editor integration and backend security API communication (`CodeEditor.js`).
- **Analysis Visualization**: Real-time line-marker mapping and vulnerability result displays.

### 2. UI/UX Designer & Feature Specialist (Person 2)
- **Design System**: Global CSS theme tokens, glassmorphic effects, and responsive layout (`App.css`, `index.css`).
- **Onboarding Interface**: Landing page design with particles and scroll animations (`GetStartedPage.js`).
- **User Authentication**: Secure Login/Signup interfaces and form logic (`AuthPage.js`).
- **Personalization**: Theme switcher implementation and integration (`ThemeSwitcher.js`).

---

## Project Structure

```text
src/
├── components/
│   ├── AuthPage.js        <- Authentication (Login/Signup)
│   ├── CodeEditor.js      <- Main Dashboard & Analysis
│   ├── GetStartedPage.js  <- Landing Page
│   └── ThemeSwitcher.js   <- Theme Selection UI
├── App.js                 <- Root Component & Routing
├── App.css                <- Main Styling
└── index.js               <- Entry Point
```

## Built With

- **React.js**: Modern component-based architecture.
- **Monaco Editor**: High-performance code editor for the web.
- **FastAPI**: Communication with the Python-based security engine.
- **Vanilla CSS**: Custom-tuned aesthetics without bloated frameworks.
