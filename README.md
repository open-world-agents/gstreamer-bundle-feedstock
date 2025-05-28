About gstreamer-bundle-feedstock
========================

Feedstock license: [MIT](https://github.com/open-world-agents/gstreamer-bundle-feedstock/blob/main/LICENSE)

Home: https://github.com/open-world-agents/open-world-agents

Package license: MIT

Summary: Meta-package with GStreamer-related dependencies for Open World Agents

*Note: This README is based on the conda-forge feedstock template.*

Current build status
====================


<table><tr><td>All platforms:</td>
    <td>
      <a href="https://github.com/open-world-agents/gstreamer-bundle-feedstock/actions/workflows/conda-publish.yml">
        <img src="https://github.com/open-world-agents/gstreamer-bundle-feedstock/actions/workflows/conda-publish.yml/badge.svg">
      </a>
    </td>
  </tr>
</table>

Current release info
====================

| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-gstreamer--bundle-green.svg)](https://anaconda.org/open-world-agents/gstreamer-bundle) | [![Conda Downloads](https://img.shields.io/conda/dn/open-world-agents/gstreamer-bundle.svg)](https://anaconda.org/open-world-agents/gstreamer-bundle) | [![Conda Version](https://img.shields.io/conda/vn/open-world-agents/gstreamer-bundle.svg)](https://anaconda.org/open-world-agents/gstreamer-bundle) | [![Conda Platforms](https://img.shields.io/conda/pn/open-world-agents/gstreamer-bundle.svg)](https://anaconda.org/open-world-agents/gstreamer-bundle) |

Installing gstreamer-bundle
===========================

Installing `gstreamer-bundle` from the `open-world-agents` channel can be achieved by adding `open-world-agents` to your channels with:

```
conda config --add channels open-world-agents
conda config --set channel_priority strict
```

Once the `open-world-agents` channel has been enabled, `gstreamer-bundle` can be installed with `conda`:

```
conda install open-world-agents::gstreamer-bundle
```

or with `mamba`:

```
mamba install open-world-agents::gstreamer-bundle
```

It is possible to list all of the versions of `gstreamer-bundle` available on your platform with `conda`:

```
conda search gstreamer-bundle --channel open-world-agents
```

or with `mamba`:

```
mamba search gstreamer-bundle --channel open-world-agents
```

Alternatively, `mamba repoquery` may provide more information:

```
# Search all versions available on your platform:
mamba repoquery search gstreamer-bundle --channel open-world-agents

# List packages depending on `gstreamer-bundle`:
mamba repoquery whoneeds gstreamer-bundle --channel open-world-agents

# List dependencies of `gstreamer-bundle`:
mamba repoquery depends gstreamer-bundle --channel open-world-agents
```

About open-world-agents
=======================

open-world-agents is a conda channel of installable packages for Open World Agents.
In order to provide high-quality builds, the process has been automated using GitHub Actions.
The open-world-agents organization contains one repository for each of the installable packages. 
Such a repository is known as a *feedstock*.

A feedstock is made up of a conda recipe (the instructions on what and how to build
the package) and the necessary configurations for automatic building using GitHub Actions.
It is possible to build and upload installable packages to the
[open-world-agents](https://anaconda.org/open-world-agents) [anaconda.org](https://anaconda.org/)
channel for Linux, Windows and OSX respectively.

This project uses patterns and tooling inspired by [conda-forge](https://conda-forge.org/).

**open-world-agents** - the place where the feedstock lives and works to
                       produce the finished article (built conda distributions)


Updating gstreamer-bundle-feedstock
===================================

If you would like to improve the gstreamer-bundle recipe or build a new
package version, please fork this repository and submit a PR. Upon submission,
your changes will be run on the appropriate platforms to give the reviewer an
opportunity to confirm that the changes result in a successful build. Once
merged, the recipe will be re-built and uploaded automatically to the
`open-world-agents` channel, whereupon the built conda packages will be available for
everybody to install and use from the `open-world-agents` channel.
Note that all branches in the open-world-agents/gstreamer-bundle-feedstock are
immediately built and any created packages are uploaded, so PRs should be based
on branches in forks and branches in the main repository should only be used to
build distinct package versions.

In order to produce a uniquely identifiable distribution:
 * If the version of a package **is not** being increased, please add or increase
   the [``build/number``](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#build-number-and-string).
 * If the version of a package **is** being increased, please remember to return
   the [``build/number``](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#build-number-and-string)
   back to 0.

Feedstock Maintainers
=====================

* [@MilkClouds](https://github.com/MilkClouds/)
