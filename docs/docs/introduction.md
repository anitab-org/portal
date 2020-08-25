---
id: intro
title: Introduction
---

## Why?

Tinysaurus is a minimum scaffold for Docusaurus, with a "no batteries included" approach.

Mostly, this just removes the landing page and the blog, just keeping the docs for use.

If you are coming from Github Pages, it's really easy to create a single page
documentation for your project.

## Quick Start

After cloning the repository:

### Install all dependencies

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and open up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

```
$ GIT_USER=<Your GitHub username> USE_SSH=true yarn deploy
