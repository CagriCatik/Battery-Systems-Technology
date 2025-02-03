# Docusaurus + Algolia DocSearch Integration & GitHub Pages Deployment

This guide explains how to:
- Integrate Algolia DocSearch into your Docusaurus site.
- Securely manage your DocSearch API keys and related credentials using environment variables.
- Deploy your Docusaurus website on GitHub Pages.
- Automate deployments with GitHub Actions (including an optional job for triggering the DocSearch crawler).

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Environment Setup](#local-environment-setup)
   - [Using a .env File](#using-a-env-file)
4. [Integrating Algolia DocSearch into Docusaurus](#integrating-algolia-docsearch-into-docusaurus)
   - [Using the Classic Preset](#using-the-classic-preset)
   - [Without the Classic Preset](#without-the-classic-preset)
5. [GitHub Pages Deployment Configuration](#github-pages-deployment-configuration)
6. [GitHub Actions Workflow for Deployment](#github-actions-workflow-for-deployment)
   - [Setting Up GitHub Secrets](#setting-up-github-secrets)
   - [Example Workflow File](#example-workflow-file)
7. [Advanced Customizations](#advanced-customizations)
8. [Troubleshooting and Best Practices](#troubleshooting-and-best-practices)
9. [Conclusion](#conclusion)

---

## 1. Overview

Algolia DocSearch provides an instant-search experience on documentation websites. Docusaurus comes with built-in support for DocSearch when using the classic preset. This documentation covers both the integration process and the secure management of credentials. Since the search-only API key is public, it can be safely included in your configuration—but any admin or crawler keys must be kept secret via environment variables and GitHub Secrets.

*References: , *

---

## 2. Prerequisites

- **Docusaurus Website:** A functioning Docusaurus site (v2 or v3).
- **Publicly Accessible Site:** Your website must be available online (Algolia’s crawler needs access).
- **Algolia DocSearch Credentials:** An approved Algolia account with the following credentials:
  - `APP_ID`
  - `SEARCH_API_KEY` (search-only key)
  - `INDEX_NAME`
- **Node.js and npm/yarn installed.**

*References: *

---

## 3. Local Environment Setup

### Using a .env File

To keep sensitive information secure during local development, you can store your Algolia credentials in a `.env` file in the root of your project.

1. **Create a `.env` file:**

   ```env
   # .env
   ALGOLIA_APP_ID=YOUR_APP_ID
   ALGOLIA_API_KEY=YOUR_SEARCH_API_KEY
   ALGOLIA_INDEX_NAME=YOUR_INDEX_NAME
   ```

2. **Install dotenv (if not already installed):**

   ```bash
   npm install dotenv --save
   ```

3. **Load the .env File in `docusaurus.config.js`:**

   Modify your configuration file to import and use these environment variables:

   ```js
   // docusaurus.config.js
   import 'dotenv/config';

   export default {
     title: 'My Site',
     url: 'https://your-github-username.github.io',
     baseUrl: '/',
     organizationName: 'your-github-username', // GitHub username or org name
     projectName: 'your-project-name',         // Repository name
     // Other configuration options...

     themeConfig: {
       algolia: {
         appId: process.env.ALGOLIA_APP_ID,
         apiKey: process.env.ALGOLIA_API_KEY,
         indexName: process.env.ALGOLIA_INDEX_NAME,
         contextualSearch: true,
         searchParameters: {},
         placeholder: 'Search documentation...',
         searchPagePath: 'search',
       },
       navbar: {
         items: [
           // Add the search bar to the navbar
           { type: 'search', position: 'right' },
         ],
       },
     },
   };
   ```

*References: *

---

## 4. Integrating Algolia DocSearch into Docusaurus

### Using the Classic Preset

If you use the `@docusaurus/preset-classic`, DocSearch integration is built in. Simply add the `algolia` configuration to your `docusaurus.config.js` (as shown above) to enable the search bar.

### Without the Classic Preset

If you are not using the classic preset:

1. **Install the DocSearch Theme Package:**

   ```bash
   npm install --save @docusaurus/theme-search-algolia
   # or using yarn:
   yarn add @docusaurus/theme-search-algolia
   ```

2. **Register the Theme in Your Config:**

   ```js
   // docusaurus.config.js
   export default {
     title: 'My Site',
     themes: ['@docusaurus/theme-search-algolia'],
     themeConfig: {
       algolia: {
         appId: process.env.ALGOLIA_APP_ID,
         apiKey: process.env.ALGOLIA_API_KEY,
         indexName: process.env.ALGOLIA_INDEX_NAME,
         contextualSearch: true,
         searchParameters: {},
       },
     },
   };
   ```

*References: *

---

## 5. GitHub Pages Deployment Configuration

When deploying on GitHub Pages, update your `docusaurus.config.js` with the correct URL and repository settings:

```js
// docusaurus.config.js
export default {
  url: 'https://your-github-username.github.io',
  baseUrl: '/',
  organizationName: 'your-github-username', // GitHub username or organization name
  projectName: 'your-project-name',         // Repository name
  trailingSlash: false,
  // Other settings (including themeConfig with Algolia DocSearch)
};
```

Also, add a `.nojekyll` file in your `static` folder to prevent GitHub Pages from ignoring files starting with underscores.

*References: *

---

## 6. GitHub Actions Workflow for Deployment

Automate your build and deployment process using GitHub Actions.

### Setting Up GitHub Secrets

1. Navigate to your repository on GitHub.
2. Go to **Settings > Secrets and variables > Actions**.
3. Add the following secrets:
   - `ALGOLIA_APP_ID`
   - `ALGOLIA_API_KEY`
   - *(Optional)* `ALGOLIA_ADMIN_API_KEY` (if you run a crawler that requires admin privileges)

### Example Workflow File

Create a file at `.github/workflows/deploy.yml` with the following content:

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

      - name: Upload build artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    runs-on: ubuntu-latest
    needs: build
    permissions:
      pages: write
      id-token: write

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  crawler:
    # Optional: Trigger the DocSearch crawler after deployment.
    runs-on: ubuntu-latest
    needs: deploy
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install jq
        run: sudo apt-get install -y jq

      - name: Run DocSearch Scraper
        env:
          ALGOLIA_APP_ID: ${{ secrets.ALGOLIA_APP_ID }}
          ALGOLIA_API_KEY: ${{ secrets.ALGOLIA_API_KEY }}
          # Uncomment if using an admin key:
          # ALGOLIA_ADMIN_API_KEY: ${{ secrets.ALGOLIA_ADMIN_API_KEY }}
        run: |
          docker run -it --env-file=.env \
            -e "CONFIG=$(cat ./algoliaConfig.json | jq -r tostring)" \
            algolia/docsearch-scraper
```

**Notes:**
- **Build Job:** Installs dependencies, builds your site, and creates a `.nojekyll` file.
- **Deploy Job:** Uses the [deploy-pages](https://github.com/actions/deploy-pages) action to push your build output to the `gh-pages` branch.
- **Crawler Job:** (Optional) Runs the DocSearch scraper using Docker. Adjust the script and configuration file (`algoliaConfig.json`) as needed.

*References: , *

---

## 7. Advanced Customizations

### Customizing the Search Experience

- **Contextual Search:**  
  Ensure that search results are filtered by version and language by enabling `contextualSearch`.

- **Additional Search Parameters:**  
  For instance, to filter by language or version, you can add:

  ```js
  searchParameters: {
    facetFilters: ['language:en', 'version:current'],
  }
  ```

- **Custom Placeholder:**  
  Modify the search bar placeholder text with:

  ```js
  placeholder: 'Search documentation...',
  ```

### Swizzling the SearchBar Component

If you require deep customization of the search UI:
1. Run the swizzle command:

   ```bash
   npm run swizzle @docusaurus/theme-search-algolia SearchBar
   ```

2. Edit the generated component in `src/theme/SearchBar`.

*References: *

---

## 8. Troubleshooting and Best Practices

- **No Search Results:**
  - Verify that your site is publicly accessible.
  - Check that the correct Algolia credentials are loaded from your `.env` file (or GitHub Secrets in production).
  - Confirm that your Algolia index includes the appropriate facets (e.g., `docusaurus_tag`, `language`, `version`).

- **Environment Variables Exposure:**
  - Remember that the search-only API key is safe to commit.
  - For any admin keys or crawler-specific credentials, always use environment variables and GitHub Secrets.

- **Deployment Issues:**
  - Test your production build locally using:
    ```bash
    npm run build
    npm run serve
    ```
  - Ensure that your repository’s GitHub Pages settings point to the correct branch (typically `gh-pages`).

*References: *

---

## 9. Conclusion

By following this guide, you have:
- Integrated Algolia DocSearch with your Docusaurus website.
- Secured your API credentials using a local `.env` file and GitHub Secrets.
- Configured your site for deployment on GitHub Pages.
- Automated the build and deployment process with GitHub Actions (including an optional DocSearch crawler job).

This setup not only enhances the user experience with robust search functionality but also maintains best practices in securing and automating your deployments.

For more detailed information, refer to:
- [Docusaurus Search Documentation](https://docusaurus.io/docs/search) 
- [Algolia DocSearch Documentation](https://docsearch.algolia.com/) 
