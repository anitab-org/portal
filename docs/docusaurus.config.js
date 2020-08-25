module.exports = {
  title: "Portal",
  tagline: "Minimal scaffold for Docusaurus",
  url: "https://your-docusaurus-test-site.com",
  baseUrl: "/",
  onBrokenLinks: "throw",
  favicon: "img/favicon.ico",
  organizationName: "anitab-org", // Usually your GitHub org/user name.
  projectName: "portal", // Usually your repo name.
  themeConfig: {
    colorMode: {
      defaultMode: "dark",
    },
    navbar: {
      title: "AnitaB Portal Docs",
      logo: {
        alt: "My Site Logo",
        src: "img/logo.svg",
      },
      items: [
        {
          href: "https://anitab.org/",
          label: "Anita-B.org",
          position: "right",
        },
        {
          href: "https://github.com/anitab-org/portal",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      copyright: `Copyright © ${new Date().getFullYear()} Anita-B. Built with Docusaurus.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          routeBasePath: "/",
          // It is recommended to set document id as docs home page (`docs/` path).
          homePageId: "home-page",
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl: "https://github.com/anitab-org/portal/edit/master/docs/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
