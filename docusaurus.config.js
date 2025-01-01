// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).

import { themes as prismThemes } from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Battery Management System', // Title for your website
  tagline: 'Bring your Knowledge to another level', // Tagline for your website
  favicon: 'img/favicon.ico',

  // Corrected URL
  url: 'https://CagriCatik.github.io',
  
  // Assuming you're deploying a project site
  baseUrl: '/BMS/',

  organizationName: 'CagriCatik', // GitHub org/user name
  projectName: 'BMS', // Repo name
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/CagriCatik/BMS/edit/main/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/CagriCatik/BMS/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  // Updated KaTeX CSS to a newer version
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.15.3/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-R4556vVJtIc0EJ3NKnM5ePcM78Zv5e+/ff+f6aZwYzZjnj84pK8i0PZyNnO+g0OQ',
      crossorigin: 'anonymous',
    },
  ],

  themeConfig:
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: '',
        logo: {
          alt: '',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            type: 'docSidebar',
            sidebarId: 'codesSidebar', // from sidebars.js
            position: 'left',
            label: 'Codes',
          },
          {
            to: '/blog',
            label: 'Blog',
            position: 'left',
          },
          {
            href: 'https://github.com/CagriCatik/BMS',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} BMS, Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
