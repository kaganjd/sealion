# Docs

Sea Lion's documentation site is built with [Docusaurus](https://docusaurus.io). I've included links to their docs below where I think they might be helpful.

- `docs/` are the source files for the documentation site; you'll make changes to the files in that directory
- `website/` is where the built files end up; this is the directory that's deployed to gh-pages
- Docusaurus has its own [markdown](https://docusaurus.io/docs/en/doc-markdown) conventions for file headers and other content; check them out if your formatting is not turning out the way you expected it to

## Adding docs

### API

See [API doc sample](./api_sample.md)

- create a filename formatted like `api-<WHATEVER-THE-EXAMPLE-IS>.md`
- create an `id`, which should be the same as the filename without the `.md` extension
- create a `title` that includes either "Method" or "Property"
- create a `sidebar_label`, which should be the same as the title but without "Method" or "Property" (since it will already be under one of those headings)

The API documentation you write should start with a high-level description of the method or property. What does it do? Does it return anything? If it returns an object, include an example of the kind of object it returns.

Next, the API doc should have a "Usage" section with a short example of how the method or property is written in code. After the code block, describe more specifically than you did above what exactly this method or property does.

Next, the API doc should have a "Parameters" section. The format of this is:

`parameterThatsPassed`_TypeOfObject_. A short description of what the parameter is, in regular words.

where _TypeOfObject_ may be a string, integer, boolean, etc.

### Examples

See [Example doc sample](./examples_sample.md)

- create a filename formatted like `api-<WHATEVER-THE-EXAMPLE-IS>.md`
- create an `id`, which should be the same as the filename without the `.md` extension
- create a `title`
- create a `sidebar_label`, which should be the same as the title

The example itself should include code (and comments) that could be copy/pasted into the p5 web editor and run.

## Running the website

[Docusaurus](https://docusaurus.io/docs/en/installation#running-the-example-website)

- `$ cd website/`
- `$ npm run start` opens your default browser to a local server on port 3000 so you can see your changes

## Build and publish

[Docusaurus](https://docusaurus.io/docs/en/publishing#using-github-pages)

- `$ cd website/`
- `$ npm run build` builds the docs site
- to publish the latest build to gh-pages branch (requires push access to the repo), copy and paste this into the command line, replacing `<GIT_USER>` with your Github username:

```
$ GIT_USER=<GIT_USER> \
  CURRENT_BRANCH=master \
  USE_SSH=true \
  npm run publish-gh-pages
```
