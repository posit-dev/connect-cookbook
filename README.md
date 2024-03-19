# connect-cookbook

🧑‍🍳 Recipes for working with the Posit Connect API and SDKs

## Goals

* Empower publishers and admins to get more value out of Connect by provide small, concrete code examples that do useful things with the API using our Python and R SDKs.
* Ensure that the code examples work using the latest versions of Connect and our SDKs.
* Guide the development of the SDKs and Connect by identifying areas for improvement.

## Proposed design

> Not set in stone! Probably wrong on some points! Please make issues/PRs to fix this!

This repository hosts a quarto site. Each subdirectory is a recipe, containing an `index.qmd` with prose describing the workflow, and `.py` and/or `.R` scripts, which are included in the rendered recipe page in a tabbed view.

* We may want the scripts to be [Quarto scripts](https://quarto.org/docs/computations/render-scripts.html), i.e. .py or .R files with annotations that make nice HTML output if you run them with Quarto, but that also run fine on their own.
* Scripts should be downloadable from the recipe page.

We've had some discussion about how or where more full examples of content would go, like functioning Shiny apps or Quarto reports. It's possible they could also live here, though testing may be more challenging.

## CI and Testing

Scripts should be tested using a containerized Connect populated with basic users and content. If script output is shown in the recipes, this environment should also be use to render the docs.

Some brainstorming for the CI setup:

* Use jumpstart examples as the content?
* Update image nightly/on schedule, and use the cached image when testing the recipes (i.e. not having to re-upload all of the content via the API)
* Running with secrets in GHA, but should also be able to run locally easily
* Could be a server deployed somewhere instead of containers, but we'd probably want the content/data reset each time we rebuild the cookbook since some recipes may modify.
    * Recipes should generally be robust to changes in global state they may face, since they could be run out of order or run multiple times
    * Should recipes have teardowns that restore state?
* Should also be able to point scripts against another test server (e.g. when writing scripts for not-yet-released features, or for configurations not set up in the base image)

