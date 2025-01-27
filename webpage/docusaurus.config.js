// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).

import { themes as prismThemes } from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: ' Battery Systems and Technology', // Title for your website
  tagline: 'Bring your Knowledge to another level', // Tagline for your website
  favicon: 'img/favicon.ico',

  // Corrected URL
  url: 'https://CagriCatik.github.io',
  
  // Assuming you're deploying a project site
  baseUrl: '/Battery-Systems-Technology/',

  organizationName: 'CagriCatik', // GitHub org/user name
  projectName: 'Battery-Systems-Technology', // Repo name
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
          editUrl: 'https://github.com/CagriCatik/Battery-Systems-Technology/edit/main/',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/CagriCatik/Battery-Systems-Technology/edit/main/',
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
      image: 'img/undraw_online.svg',
      navbar: {
        title: '',
        logo: {
          alt: '',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'fundamentalsSidebar',
            position: 'left',
            label: 'Fundamentals of Battery Technology',
          },
          {
            type: 'docSidebar',
            sidebarId: 'agingDegradationSidebar',
            position: 'left',
            label: 'Aging and Degradation',
          },
          {
            type: 'docSidebar',
            sidebarId: 'chemistrySidebar',
            position: 'left',
            label: 'Chemistry and Design Principles',
          },
          {
            type: 'docSidebar',
            sidebarId: 'batteryPackSidebar',
            position: 'left',
            label: 'Battery Pack Engineering',
          },
          {
            type: 'docSidebar',
            sidebarId: 'thermalManagementSidebar',
            position: 'left',
            label: 'Thermal Management',
          },
          {
            type: 'docSidebar',
            sidebarId: 'characteristicsSidebar',
            position: 'left',
            label: 'Characteristics and Technical Specifications',
          },
          {
            type: 'docSidebar',
            sidebarId: 'sizingOptimizationSidebar',
            position: 'left',
            label: 'Sizing and Optimization',
          },
          {
            type: 'docSidebar',
            sidebarId: 'batteryManagementSidebar',
            position: 'left',
            label: 'Battery Management System',
          },
          {
            type: 'docSidebar',
            sidebarId: 'bmsDesignArchitectureSidebar',
            position: 'left',
            label: 'Design and Architecture',
          },
          {
            type: 'docSidebar',
            sidebarId: 'modelingTestingSidebar',
            position: 'left',
            label: 'Modeling and Testing',
          },
          {
            type: 'docSidebar',
            sidebarId: 'glossarySidebar',
            position: 'left',
            label: 'Glossary',
          },

        ],
      },

      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} Battery Systems and Technology`,
        links: [
          {
            label: 'GitHub',
            href: 'https://github.com/CagriCatik/Battery-Systems-Technology',
          },

          {
            to: '/blog',
            label: 'Blog',
            position: 'left',
          },
        ],
      },
      
      
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
