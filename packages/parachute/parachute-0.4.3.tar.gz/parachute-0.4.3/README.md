Parachute
=========

Parachute is a swiss army knife for ArduPilot settings. It helps you quickly and
easily back up all your parameters to a file (and restore them). It also lets
you get/set them, filter them, diff them, restore them or convert them to
parameter files compatible with Mission Planner/QGroundControl.


Installation
------------

Installing Parachute is simple. You can use `pipx` (recommended):

```bash
$ pipx install parachute
```

Or `pip` (less recommended):

```bash
$ pip install parachute
```

You can also download pre-built binaries for Windows and Linux from the
[artifacts page](https://gitlab.com/stavros/parachute/-/pipelines).


Usage
-----

Parachute is called like so:

```bash
$ parachute backup <craft name>
```

For example:

```bash
$ parachute backup Mini-Drak
```

To restore:

```bash
$ parachute restore backup.chute
```


Conversion
----------

You can also convert a Parachute file to a file compatible with Mission Planner or QGroundControl:

```bash
$ parachute convert qgc Mini-Drak_2021-03-02_02-29.chute Mini-Drak.params
```


Filtering
---------

You can filter parameters based on a regular expression:

```bash
$ parachute filter "serial[123]_" Mini-Drak_2021-03-02_02-29.chute filtered.chute
```

Since all parameter names are uppercase, the regex is case-insensitive, for convenience.

You can also filter when converting:

```bash
$ parachute convert --filter=yaw mp Mini-Drak_2021-03-02_02-29.chute -
```


Comparing
---------

You can compare parameters in a backup with parameters on the craft:

```bash
$ parachute compare backup.chute
```


Getting/setting
---------------

You can get and set parameters:

```bash
$ parachute get BATT_AMP_OFFSET BATT_AMP_PERVLT
```

```bash
$ parachute set BATT_AMP_OFFSET=-0.0135 BATT_AMP_PERVLT=63.8826
```

You can get and set a single bit like so:

```bash
$ parachute get --binary FLIGHT_OPTIONS
```

```bash
$ parachute set FLIGHT_OPTIONS:5=1
```


Shell completions
------------------

Parachute includes shell completion for AP parameters for various shells.  After you've
enabled completions, you can get parameter completion for the `get` and `set` commands.
For example, try typing `parachute get acr<TAB>`.

The way to enable it depends on your shell:


### fish

Save the completion script to ~/.config/fish/completions/parachute.fish:

```bash
_PARACHUTE_COMPLETE=fish_source parachute > ~/.config/fish/completions/parachute.fish
```


### bash

Save the completion script somewhere.

```bash
_PARACHUTE_COMPLETE=bash_source parachute > ~/.parachute-complete.bash
```

Source the file in ~/.bashrc.

```bash
. ~/.parachute-complete.bash
```


### zsh

Save the completion script somewhere.

```bash
_PARACHUTE_COMPLETE=zsh_source parachute > ~/.parachute-complete.zsh
```

Source the file in ~/.zshrc.

```bash
. ~/.parachute-complete.zsh
```

# Changelog


## v0.4.3 (2023-01-27)

### Fixes

* Complain if `get` and `set` are mixed up. [Stavros Korokithakis]


## v0.4.2 (2023-01-07)

### Features

* Add the `force-accept-calibration` command. [Stavros Korokithakis]

### Fixes

* Fix parameter display order. [Stavros Korokithakis]


## v0.4.1 (2022-11-05)

### Features

* Don't exit on missing parameters when restoring. [Stavros Korokithakis]

### Fixes

* Fix bug where negative numbers were erroneously not accepted. [Stavros Korokithakis]


## v0.4.0 (2022-07-02)

### Features

* Add getting and setting bits directly. [Stavros Korokithakis]

* Add the "--binary" parameter to display bit indexes. [Stavros Korokithakis]

### Fixes

* Remove unused code. [Stavros Korokithakis]


## v0.3.11 (2022-02-26)

### Features

* Add "--compare" flag to "restore" [Stavros Korokithakis]

### Fixes

* Name files a bit better. [Stavros Korokithakis]


## v0.3.10 (2021-12-17)

### Fixes

* Improve autodetection even more again. [Stavros Korokithakis]

* Improve autodetection even more. [Stavros Korokithakis]

* Improve autodetection default. [Stavros Korokithakis]


## v0.3.9 (2021-11-02)

### Fixes

* Show the correct parameter name when diffing. [Stavros Korokithakis]


## v0.3.8 (2021-10-29)

### Features

* Colorize tables. [Stavros Korokithakis]

* Make table Markdown-compatible. [Stavros Korokithakis]

### Fixes

* Fix inverted `compare` display. [Stavros Korokithakis]


## v0.3.7 (2021-10-23)

### Features

* Include parameter completions. [Stavros Korokithakis]

* Add `--baud-rate` cli option` [Stavros Korokithakis]

### Fixes

* Display accurate names when diffing. [Stavros Korokithakis]

* Fix port detection on Windows. [Stavros Korokithakis]


## v0.3.6 (2021-08-29)

### Fixes

* Make messages more consistent. [Stavros Korokithakis]


