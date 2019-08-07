# Nano Protocol Documentation

`nano-docs` is the source code for the Nano protocol documentation and is built using [MkDocs](https://www.mkdocs.org/) with the [MkDocs Material theme](https://squidfunk.github.io/mkdocs-material/).

### Purpose
This documentation is focused on various users within the technical community: advanced users, node operators, developers integrating Nano, and those interested in details around how the protocol works. All efforts to help update the documentation should keep in mind these goals as submissions that fall outside of this scope are likely to be rejected.

### Contributing
If you want to help with updating documentation, we recommend you join the Discord (https://chat.nano.org) #documentation channel to keep up to date on the latest activity. GitHub issues will be used to manage requests for changes. It is recommended any navigational changes or larger updates be discussed on the Discord #nano-docs channel or within a GitHub issue before work is completed - this will help avoid work being wasted if it doesn't align with the documentation goals.

To submit changes, please fork the repository and create a branch to make your changes in. Submit a Pull Request back to the source repository when ready and they will be reviewed for possible inclusion.

## Development
The recommended local setup is to use Docker with a pre-built image for MkDocs and Material theme. With Docker installed, from your nano-docs directory run:

`docker pull squidfunk/mkdocs-material`

`docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material`

You can also install MkDocs with Python 3 to serve using the following:

``` 
pip install -r requirements.txt
mkdocs serve
```

Access the site at http://localhost:8000. This supports automatic rebuilding so anytime you save changes to the documentation or configuration it will be rebuilt and refresh the page for you. Some search indexing may remain cache between builds.

## Formatting and Organization Tips

### Headers
Pages automatically have a `<h1>` title setup for them based on the page name so headers `##` (`<h2>`) and higher should only be used to organize the content.

### Table of Contents
Currently the ToC on the right side is limited to a depth of 4, so `##`, `###` and `####` will be included there. Higher header levels can be used on the page ot better organize content but will not be in the ToC.

### Snippets
The `snippets` folder contains reusable pieces of content which can be inserted as follows:

`--8<-- "snippet-file-name.md"`

This should be used for simple, duplicated content only and is not a complex templating setup.

### Comments
The StripHTML extension is used so HTML-style comments can be included in the markdown docs, although for best compatibility you should keep them at the top level, not within indented areas/rendered admonition blocks, etc. as much as possible.

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
Support has been added for Mermaid Sequence Diagrams, documentation can be found here: https://mermaidjs.github.io/sequenceDiagram.html