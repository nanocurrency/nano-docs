# Nano Protocol Documentation

`nano-docs` is the source code for the Nano protocol documentation and is built using [MkDocs](https://www.mkdocs.org/) with the [MkDocs Material theme](https://squidfunk.github.io/mkdocs-material/).

### Purpose
This documentation focuses on various users within the technical community: advanced users, node operators, developers integrating Nano, and those interested in details around how the protocol works. All efforts to help update the documentation should keep in mind these goals as submissions that fall outside of this scope are likely to be rejected.

### Contributing
For users wishing to contribute to this documentation, we recommend you join the Discord (https://chat.nano.org) #documentation channel to keep up to date on the latest activity. GitHub issues will be used to manage requests for changes. It is recommended any navigational changes or larger updates be discussed on the Discord #nano-docs channel or within a GitHub issue before completing work - this will help avoid wasted work that does not align with the documentation goals.

To submit changes, please fork the repository and create a branch to make changes. Submit a Pull Request back to the source repository when ready for review ahead of possible inclusion.

## Development
The recommended local setup is to use Docker with a pre-built image for MkDocs and Material theme. With Docker installed, from the cloned nano-docs directory run:

```bash
docker pull nanocurrency/nano-docs:base
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs nanocurrency/nano-docs:base
```

You can also install MkDocs with Python 3 to serve using the following:

```bash
pip3 install -r requirements.txt
mkdocs serve
```

Access the site at http://localhost:8000. This supports automatic rebuilding, so anytime changes are saved to the documentation or configuration, it will be rebuilt and refresh the page. Some search indexing may remain cache between builds.

## Formatting and Organization Tips

### Headers
Pages automatically have a `<h1>` title setup for them based on the page name, so headers `##` (`<h2>`) and higher should only be used to organize the content.

### Table of Contents
Currently, the ToC on the right side is limited to a depth of 4, so `##`, `###', and `####` will be included there. Higher header levels can be used on the page to better organize content but will not be in the ToC.

### Links
MkDocs has a link checker built in that can be run using the `--strict` flag on `mkdocs serve`, or `mkdocs build` command. This flag is included in the build pipeline. For it to work, links must be referencing the relative file path with the file extension included and no trailing slashes. Anchors are not included in this check. Although relative URLs will function if used, they will not be verified by the link checker.

For example, linking from a page in the`running-a-node` folder to `integration-guides` would be:

* Gets checked: `../integration-guides/the-basics.md`.
* Doesn't get checked: `/integration-guides/the-basics`

### Snippets
The `snippets` directory contains reusable pieces of content which can be inserted as follows:

`--8<-- "snippet-file-name.md"`

This should be used for simple, duplicated content only and is not a complex templating setup.

### Comments
The StripHTML extension is used so that HTML-style comments can be included in the markdown docs. However, for best compatibility, keep them at the top level, not within indented areas/rendered admonition blocks, etc. as much as possible.

`<!-- this is a valid comment that will not get rendered to the browser -->`

### Admonition Extension Quick Reference
Admonition is an extension for MkDocs that provides easy block-styled side content (including collapsible blocks). More details on use can be found here: https://squidfunk.github.io/mkdocs-material/extensions/admonition/. Below is a quick reference for this functionality:

For an always expanded option:
`!!! note "This is the title"
	 This is the text`

For a collapsible option:

`??? question "Is this collapsed by default?"
	 Yes, it is`

`???+ question "Is this expanded by default?"
	 Yes, it is`

Types include:

- note
- abstract
- info
- tip
- success
- question
- warning
- failure
- danger
- bug
- example
- quote

### Mermaid Sequence Diagrams
There is support for Mermaid Sequence Diagrams, and documentation can be found here: https://mermaidjs.github.io/#/sequenceDiagram

### Octicon icons
The scripts for using Github's Octicons are included in the header. Details for available icons can be found here: https://primer.style/octicons/. Usage should be limited. Example currently available in announcement block:

`<span class="iconify" data-icon="octicon-tag-16" data-inline="false"></span>`
