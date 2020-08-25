---
id: adding-pages
title: Adding Pages
---

To create a page:

- Simply add a Markdown file `.md` to `docs/`
- Make sure to add the frontmatter at the top of the page:

Example:

```
---
id: adding-pages
title: Adding Pages
---
```
- Finally, to add to the sidebar, add a new entry to `sidebars.js`:

```
{
      type: "doc",
      id: "adding-pages",
},
```

Here's the [commit](https://github.com/SanketDG/tinysaurus/commit/f7af055a85d51c26a0175fa23b45c6f58e3a1b5e) that adds this page!
