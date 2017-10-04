# Hail Community Contributions

[![PyPI](https://img.shields.io/pypi/v/hailc.svg)](https://pypi.python.org/pypi/hailc)

Lightly reviewed community code snippets for [Hail](https://www.hail.is).

Browse the current submissions here:

- [**Submissions for Hail 0.1**](./hailc/v01/)

## Goals

Although the flexibility and functionality of the core Hail repository is 
growing quickly, the amount of useful functionality produced by Hail users 
is growing far faster. This repository is an attempt to make it easier 
for Hail users to share their hard work, which will hopefully lead to 
more rapid progress on both the software and the science for the whole 
community.

What do we expect make its way here? Utility functions, complete pipelines,
visualization methods, and more!

A website that indexes these submissions and makes them searchable will 
be created at a later date.

## Using this repository

We deploy to the [Python Package Index (PyPI)](https://pypi.python.org/pypi). 
This means that you can install or upgrade `hailc` with pip:

```
pip install hailc --upgrade
```

Each contributor creates a package inside the `hailc` subdirectory corresponding
to the correct version of Hail, which can be imported as follows:

```python
import hailc.v01.tpoterba as tp
```

The correct import statement should be listed at the top of each contributor's
README.md file.

## Submission guidelines

1. **Version control process.** Make pull requests from forked copies
of the main repository. Here's a [useful walkthrough](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/)
about how to do that. Take a look at [GitHub help](https://help.github.com/) 
for even more assistance!

2. **Approval process.** Initially, Hail team members and collaborators
will review new submissions. As this experiment matures, we will be happy
to grant review authority to anyone who is an active and productive 
participant in the Hail community!

3. **Naming guidelines.** Your package should either be named after your
 GitHub username, or your name (first initial and last name, for example).

4. **README is required! Tests and extensive documentation are not.** 
This repository is only minimally reviewed -- it is a resource for the 
community, and should be maintained by the community. The README is the 
only requirement -- this is how people can look at the various modules
present. It would be nice to include at least minimal documentation about 
your submissions and describe how you tested them, but submissions will
not be rejected without these.

5. **No automatic monkey-patching!** This is the only code rule -- don't
automatically modify Hail classes or methods at import time. However, you can
include an explicit `patch` function to do this, as long as you document it
in your README. To a user, the patching will look something like this:

    ```
    import hailc.v01.tpoterba as tp
    tp.patch()
    ```

6. **Example submission.** If you're wondering what a submission might
look like, take a look at the [example](./example). From the repository
head, you can copy this into a new folder for your package from the
command line:

    ```
    cp -r example hailc/v01/mypkg
    ```

7. **Style.** Try to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/). 
You may be asked to reformat egregiously unreadable code, but otherwise feel
free to submit code as you use it yourself.