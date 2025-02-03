# Docusaurus Authentication & Sign In Integration

This guide covers:

- Setting up environment variables for authentication credentials.
- Configuring Firebase Authentication.
- Integrating Firebase into your Docusaurus site via component swizzling.
- Creating login, logout, and auth-check components.
- Deploying your site (with secure API key management) on GitHub Pages.
- (Optional) Automating deployment with GitHub Actions.

*References: , , *

---

## 1. Overview

Docusaurus is a static site generator built with React. Although it does not include authentication by default, you can add a sign in feature by “swizzling” (overriding) the top‑level `<Root>` component and integrating an authentication library. In this documentation we use [Firebase Authentication](https://firebase.google.com/docs/auth) with Email/Password (or other providers) to secure access to your documentation. You will also learn how to protect your Firebase credentials by using a local .env file during development and GitHub Secrets in production.

*Note:* The search-only API keys for services like DocSearch are public. For authentication providers, you must secure any private keys.

---

## 2. Prerequisites

- A working Docusaurus site (v2 or v3)  
- Node.js and npm (or yarn) installed  
- A Firebase account (with a Firebase project)  
- Basic familiarity with React and Firebase  
- (Optional) GitHub repository and GitHub Pages configuration for deployment

*References: *

---

## 3. Local Environment Setup

### 3.1 Create a Local Environment File

Store your Firebase configuration values in a `.env` file. For example, create a file named `.env.local` at the project root:

```env
# .env.local
FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
FIREBASE_APP_ID=your-firebase-app-id
```

### 3.2 Install Required Packages

Install Firebase and a helper UI library (such as react-firebaseui) as well as a plugin to load environment variables in Docusaurus:

```bash
npm install firebase@^9.22.0 react-firebaseui@^6.0.0 docusaurus-plugin-dotenv@^1.0.1
```

*References: *

### 3.3 Configure Docusaurus to Use .env

Update your `docusaurus.config.js` file to include the dotenv plugin so that your environment variables are available at build time:

```js
// docusaurus.config.js
module.exports = {
  // ...other configuration options
  plugins: [
    [
      "docusaurus-plugin-dotenv",
      {
        path: "./.env.local",
        systemvars: true, // Set to true if you wish to load system variables (useful in CI)
      },
    ],
  ],
  // GitHub Pages settings (if deploying there)
  url: "https://your-github-username.github.io",
  baseUrl: "/",
  organizationName: "your-github-username",
  projectName: "your-project-name",
};
```

---

## 4. Firebase Setup

1. **Create a Firebase Project:**  
   Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project. Follow the steps provided by Firebase.

2. **Add a Web App:**  
   In your Firebase project dashboard, click “Add app” and select the Web icon. Fill in the details and register the app. You will receive your Firebase configuration (API key, authDomain, etc.)—copy these into your `.env.local` file.

3. **Enable Authentication:**  
   Under the Authentication section, choose “Get Started” and then enable the desired sign in methods (e.g., Email/Password). Save your changes.

*References: *

---

## 5. Integrating Firebase into Docusaurus

Since Docusaurus is built with React, you can integrate Firebase authentication by swizzling the top‑level `<Root>` component.

### 5.1 Create a Firebase Config Module

Create a configuration file (for example, at `src/config/firebase-config.js`) that reads from your environment variables:

```js
// src/config/firebase-config.js
export const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.FIREBASE_APP_ID,
};
```

### 5.2 Swizzle the Root Component

Override the `<Root>` component by creating a file at `src/theme/Root.js`. This component will wrap your site with an authentication check.

```jsx
// src/theme/Root.js
import React from "react";
import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
import { Redirect, useLocation } from "@docusaurus/router";

import { firebaseConfig } from "../config/firebase-config";
import Login from "../components/Login";
import Loading from "../components/Loading";

// Initialize Firebase app (ensure this runs only once)
initializeApp(firebaseConfig);
const auth = getAuth();

export function AuthCheck({ children }) {
  const [user, setUser] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const location = useLocation();
  const currentPath = location.pathname;

  React.useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  // Optionally, define protected paths (e.g., '/private')
  const PROTECTED_PATHS = ["/private"];

  if (loading) return <Loading />;

  // If on protected route and not authenticated, redirect to login page
  if (!user && PROTECTED_PATHS.some((path) => currentPath.startsWith(path))) {
    return <Redirect to="/login" />;
  }

  // If user is authenticated and on login page, redirect to home page
  if (user && currentPath === "/login") {
    return <Redirect to="/" />;
  }

  return children;
}

export default function Root({ children }) {
  return <AuthCheck>{children}</AuthCheck>;
}
```

*References: , *

---

## 6. Creating Authentication Components

### 6.1 Login Component

Create a login page component (e.g., `src/components/Login/index.js`). Here we use [react-firebaseui](https://github.com/firebase/firebaseui-web-react) for a quick login UI:

```jsx
// src/components/Login/index.js
import React from "react";
import StyledFirebaseAuth from "react-firebaseui/StyledFirebaseAuth";
import { getAuth } from "firebase/auth";
import "firebase/compat/auth"; // required for react-firebaseui compatibility
import "./styles.css";

const auth = getAuth();

const uiConfig = {
  signInFlow: "popup",
  signInOptions: [
    // Enable Email/Password as a sign in provider
    auth.EmailAuthProvider.PROVIDER_ID,
    // You can add other providers here (e.g., Google)
  ],
  callbacks: {
    // Avoid redirects after sign-in.
    signInSuccessWithAuthResult: () => false,
  },
};

export default function Login() {
  return (
    <div className="login-wrapper">
      <h2>Please Sign In</h2>
      <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={auth} />
    </div>
  );
}
```

Create a simple CSS file (`src/components/Login/styles.css`) to style your login page:

```css
/* src/components/Login/styles.css */
.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
```

### 6.2 Loading Component

A simple loading component helps avoid blank pages during authentication state checks.

```jsx
// src/components/Loading/index.js
import React from "react";
import "./styles.css";

export default function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner" />
    </div>
  );
}
```

And the corresponding CSS (`src/components/Loading/styles.css`):

```css
/* src/components/Loading/styles.css */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
.spinner {
  border: 4px solid rgba(0,0,0,0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #09f;
  animation: spin 1s ease infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

### 6.3 Adding a Logout Button to the Navbar

To let users sign out, override (swizzle) the Navbar component to add a Login/Logout button that reflects the current auth state. For example, modify your custom Navbar (e.g., in `src/utils/utils.js`) to include a button that calls Firebase’s signOut:

```jsx
// Example snippet for adding a Logout button (modify your Navbar swizzle accordingly)
import React, { useEffect, useState } from "react";
import { getAuth, signOut, onAuthStateChanged } from "firebase/auth";
import { useThemeConfig } from "@docusaurus/theme-common";

export function useNavbarItems() {
  const [user, setUser] = useState(null);
  const auth = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
    });
    return unsubscribe;
  }, [auth]);

  const defaultItems = useThemeConfig().navbar.items || [];
  const authItem = user
    ? { label: "Logout", to: "/logout" }
    : { label: "Login", to: "/login" };

  return [...defaultItems, authItem];
}
```

Then, in your logout route logic (which you can handle in your `AuthCheck` component or a dedicated logout page), call:

```js
// Example logout handler
signOut(auth);
```

*References: , *

---

## 7. Deploying to GitHub Pages

### 7.1 Update GitHub Pages Configuration

Ensure your `docusaurus.config.js` includes your GitHub Pages settings:

```js
// docusaurus.config.js
module.exports = {
  url: "https://your-github-username.github.io",
  baseUrl: "/",
  organizationName: "your-github-username",
  projectName: "your-project-name",
  // ...other settings...
};
```

Also, add a `.nojekyll` file in your `static` folder (or have your build process generate one) so that GitHub Pages correctly serves your static files.

### 7.2 Secure Your Environment Variables

For production, add your Firebase configuration values as GitHub Secrets and set them in your hosting environment (e.g., using Vercel, Netlify, or Render). The `docusaurus-plugin-dotenv` can load these variables during your build.

---

## 8. Automating Deployment with GitHub Actions (Optional)

Create a GitHub Actions workflow (e.g., `.github/workflows/deploy.yml`) to automate building and deploying your Docusaurus site:

```yaml
name: Deploy Docusaurus Site

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build Docusaurus site
        run: npm run build

      - name: Create .nojekyll file
        run: echo "" > build/.nojekyll

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
        with:
          path: build
```

Make sure that any sensitive keys (if used in non–public portions of your app) are stored as GitHub Secrets and injected during the build.

*References: *

---

## 9. Troubleshooting and Best Practices

- **Authentication State Delays:**  
  Use a loading indicator (as shown in the Loading component) while Firebase checks auth state.

- **Protected Routes:**  
  Define which paths require authentication in your AuthCheck component. Adjust the logic to redirect unauthenticated users to `/login`.

- **Environment Variables:**  
  Never commit your `.env.local` file with real credentials. Use GitHub Secrets for production builds.

- **Swizzling Considerations:**  
  When overriding components, make sure you maintain the original functionality for users who are not authenticated.

*References: , *

---

## 10. Conclusion

By following this guide you have:

- Secured your Firebase credentials using environment variables.
- Integrated Firebase Authentication into your Docusaurus site via component swizzling.
- Created custom Login, Logout, and AuthCheck components to manage authentication.
- Configured your site for deployment on GitHub Pages and (optionally) automated the build with GitHub Actions.

This setup enables you to add a sign in feature to your static documentation while keeping sensitive configuration secure. Customize further as needed (for example, adding additional providers or role-based access) to fit your project requirements.
