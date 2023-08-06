[![licence badge]](/LICENCE.txt)
[![pipeline status]][pipeline report]


Coverage.py Test Context Plugin
===============================

**A Coverage.py plugin module for adding test names as contexts**

Coverage reports from *Coverage.py* can include line "contexts"; strings that are attached 
to lines of code that provide some sort of contextual information to a reader.

This package consists of a dynamic context plugin for *Coverage.py* that adds unit test 
names as contexts.


Usage
-----

Add the plugins package to your test dependencies, wherever they are:
  `kodo.plugins.cover-test-context`

Then add the plugin to your `coverage` configuration:

<details><summary><strong>pyproject.toml</strong></summary>

```toml
[tool.coverage.run]
plugins = [
  "kodo.plugins.cover_test_context",
]
```

</details>

<details><summary><strong>setup.cfg, tox.ini</strong></summary>

```ini
[coverage:run]
plugins =
  kodo.plugins.cover_test_context
```

</details>

<details><summary><strong>.coveragerc</strong></summary>

```ini
[run]
plugins =
  kodo.plugins.cover_test_context
```

</details>


---

[licence badge]:
  https://img.shields.io/badge/licence-MPL--2.0-orange.svg
  "Licence: MPL-2.0"

[pipeline status]:
  https://code.kodo.org.uk/dom/cover-plugin-test-context/badges/main/pipeline.svg

[pipeline report]:
  https://code.kodo.org.uk/dom/cover-plugin-test-context/-/pipelines/latest
