/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// See https://docusaurus.io/docs/site-config for all the possible
// site configuration options.

const siteConfig = {
  title: '🌊 Sea Lion', // Title for your website.
  tagline: 'A toolkit for using network data in p5.js sketches. ARP, ARP.',
  url: 'https://kaganjd.github.io', // Your website URL
  baseUrl: '/sealion/', // Base URL for your project */
  // Used for publishing and more
  projectName: 'sealion',
  organizationName: 'kaganjd',
  // For top-level user or org sites, the organization is still the same.
  // e.g., for the https://JoelMarcey.github.io site, it would be set like...
  //   organizationName: 'JoelMarcey'

  // For no header links in the top nav bar -> headerLinks: [],
  headerLinks: [
    {doc: 'getting-started', label: 'Getting Started'},
    {doc: 'api-hostname', label: 'API'},
    {doc: 'examples-router-and-computer', label: 'Examples'},
    {blog: false, label: 'Blog'},
  ],

  /* path to images for header/footer */
  /* headerIcon: 'img/docusaurus.svg', */
  /* footerIcon: 'img/docusaurus.svg', */
  /* favicon: 'img/favicon.png', */

  /* Colors for website */
  colors: {
    primaryColor: 'purple',
    secondaryColor: 'cyan',
  },
  /* Custom fonts for website */
  /*
  fonts: {
    myFont: [
      "Times New Roman",
      "Serif"
    ],
    myOtherFont: [
      "-apple-system",
      "system-ui"
    ]
  },
  */
  highlight: {
    // Highlight.js theme to use for syntax highlighting in code blocks.
    theme: 'default',
  },
  // Add custom scripts here that would be placed in <script> tags.
  scripts: ['https://buttons.github.io/buttons.js'],
  onPageNav: 'separate',
  cleanUrl: true,

  // Open Graph and Twitter card images.
  ogImage: 'img/docusaurus.png',
  twitterImage: 'img/docusaurus.png',
};

module.exports = siteConfig;
