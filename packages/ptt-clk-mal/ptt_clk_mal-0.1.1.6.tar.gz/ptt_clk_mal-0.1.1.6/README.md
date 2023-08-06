# MALoPotatoClock

*It's my first time to write a python package.*

## Overview

> A simple potato clock inspired by tomato clock.
> > sadly, I don't have a potato, so I use a scheduled timer instead.
>
> It's a simple timer that helps you to focus on your work.

- [x] A simple timer
- [x] A simple CLI
- [x] A simple notification (for Linux only)
- [ ] A simple GUI
- [ ] A simple notification for Windows
- [ ] Recurring schedule with rests like tomato clock

## Usage

### Install

#### from PyPI

```bash
pip install mal-potato-clock
```

#### from release

```bash
pip install mal-potato-clock-<release>.tar.gz
```

#### from source (using poetry only)

```bash
git clone <url>
cd mal-potato-clock
poetry install
```

### Run

#### Run the timer

```bash
pttClk -t <time> -n <notification intervals> -a <aiming things>
```
#### history

```bash
pttClk his -q <last x days> -g <aim group>
```

#### setting

You should type below for more information.
> All commands above's help(-h) information are also available.
```bash
pttClk set -h 
```
#### Example

```bash
pttClk -t 25 -n 5 -a "study"
pttClk his -q 7 -g "study"
pttClk -s # show setting
```

### Images

![example Overview](./asserts/eg0.png)
