# news-image-20261125-entry

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/e0426685-cloud/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/e0426685-cloud/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World Today — Wednesday 25 November 2026

A single-image broadsheet front page summing up Wednesday 25 November
2026, drawn entirely by a Python program that uses only the standard
library.

## What's on the page

- **Lead story:** President Volodymyr Zelenskiy confirms Ukraine was
  behind Saturday's drone strike on a Russian cargo ship in the Gulf of
  Finland, with ally Norway urging caution — illustrated by a stylised
  cargo ship at sea.
- **Middle East:** Houthi drone strike on Riyadh's tallest tower leaves
  eleven people wounded.
- **Washington:** Donald Trump awards Rudy Giuliani the Presidential
  Medal of Freedom.
- **Technology:** Huawei found guilty of stealing trade secrets, but
  acquitted of racketeering.
- **Sport:** England level the T20 series against Australia with an
  eight-wicket win.
- **Business:** Dell lifts its forecasts on a record AI server quarter;
  Nvidia shares fall 7 percent.
- **World in brief:** NATO early-warning aircraft for Poland, a
  5.6-magnitude earthquake in Nepal, and Sarkozy's corruption case
  ordered to trial.

## How it is made

`main.py` draws the whole page pixel by pixel: a hand-built 5x7 bitmap
font renders the masthead, headlines and body copy, and a minimal PNG
encoder (zlib + struct) writes the finished 1024x1024 image. No
third-party libraries are used at all — run `python3 main.py` and it
writes the finished image to `/output/entry.png` (the location the
judge reads at grade time). For local verification, set
`MAKEFUN_OUTPUT_DIR` to write it somewhere else instead, e.g.
`MAKEFUN_OUTPUT_DIR=. python3 main.py`.

## Run it

```sh
python3 main.py
```

Writes the finished 1024x1024 broadsheet to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` when set). Python standard library only.

---

<sub>Entered on [make.fun](https://make.fun/?ref=52532a96&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
