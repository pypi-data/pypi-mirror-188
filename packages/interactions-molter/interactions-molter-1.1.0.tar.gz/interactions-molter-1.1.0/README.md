<p align="center">
  <img src="https://cdn.discordapp.com/attachments/623677414278561793/978141383804215317/interactions-molter-banner.png" alt="The banner for Molter for interactions.py." width="700"/>
</p>

<h1 align="center">Molter for interactions.py.</h1>

<p align="center">
  <a href="https://pypi.org/project/interactions-molter/">
    <img src="https://img.shields.io/pypi/v/interactions-molter" alt="PyPI">
  </a>
  <a href="https://pepy.tech/project/interactions-molter">
    <img src="https://static.pepy.tech/personalized-badge/interactions-molter?period=total&units=abbreviation&left_color=grey&right_color=green&left_text=pip%20installs" alt="Downloads">
  </a>
  <a href="https://interactions-py.github.io/molter/main/">
    <img src="https://img.shields.io/badge/docs-passing-success", alt="docs: Github Pages">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg", alt="Code style: black">
  </a>
</p>


An extension library for interactions.py to add prefixed (AKA text-based or 'message') commands. This is a demonstration of [the Molter framework](https://github.com/Astrea49/molter-core), a framework for adding prefixed commands into Discord Python libraries.

This attempts to make the prefixed command experience much like `discord.py`'s prefixed commands, though it is *not* 1:1 on purpose.

**NOTE**: This extension is primarily developed by [Astrea49](https://github.com/Astrea49).

## Installation

```
pip install interactions-molter
```

## Documentation

Documentation, including examples and an API reference, for the `main` branch (and so the latest PyPI version) can be found at [its respective Github Page](https://interactions-py.github.io/molter/main/).

For documentation for the other branches, you can look for the respective documentation [on the home page](https://interactions-py.github.io/molter/).

## Branch Explanation

- The `main` branch is the PyPI version - this branch will never deviate from it. This is done to make sure the PyPI page's example links link to the right code.
- The `beta` branch is code considered code that is stable enough to use in daily use, though it is not perfect. This branch also will target any beta, pre-release, or release candidate version of `interactions.py`, if possible.
- The `dev` branch mirrors `interactions.py`'s `unstable` branch, and is also a general testing ground for new and experimental changes. *Bugs are common on this branch. If you decide to use this branch, I highly suggest pinning to a specific commit you know is stable.*
- The `gh-pages` branch powers the documentation website, and has no Molter-related code in it.

## Credit

Thanks to both [`NAFF`](https://github.com/NAFTeam/NAFF) and [Toricane's `interactions-message-commands`](https://github.com/Toricane/interactions-message-commands) for a decent part of this! They both had a huge influence over how this port was designed.