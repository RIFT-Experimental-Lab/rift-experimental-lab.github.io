# R.I.F.T. Experimental Lab website

Static website for the laboratory, published at [rift-experimental-lab.github.io](https://rift-experimental-lab.github.io/). English is the default language; Russian and Simplified Chinese are in `ru/` and `zh/`. The language switch keeps visitors on the corresponding page.

## Build

Run from this directory:

```sh
python3 build_release.py
```

The command rebuilds all 21 pages, checks that public HTML has no preview labels or broken local links, and writes the uploadable website to `dist/`. Only the contents of `dist/` should be published. It includes `.nojekyll` for GitHub Pages and excludes scripts and `logo-compare.html`.

The site uses relative links, so the same build works at a domain root or under a repository path. No hosting URL or custom domain is hardcoded.

## Publishing

Pushing to `main` runs `.github/workflows/pages.yml`. GitHub Actions builds the site from the tracked source files and deploys `dist/` to GitHub Pages. The generated HTML and `dist/` are ignored by Git; edit the source files and push a new commit to publish an update.

## Editing

`build_demo.py` contains the Russian source pages. `localization.py` contains the English and Chinese translations. Edit those two files, then rebuild. `style.css` and `assets/rift-mark.svg` are shared by all languages. The generated HTML pages and `dist/` are outputs, not the source of record.
