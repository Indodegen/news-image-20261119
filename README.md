# The World Today — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Indodegen/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Indodegen/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A make.fun bounty entry for **news-image-20261119**: sum up 19 November's
world news in one image. Bounty page:
[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

`main.py` is a Python standard-library-only program (no PIL, no network,
no API keys). It draws a 1024×1024 newspaper front-page infographic and
writes it as a PNG. Every glyph comes from a hand-written 5×7 bitmap font
(uppercase A–Z, digits 0–9 and punctuation), scaled by integer factors,
and every icon (game controller, capitol dome, crossed missiles, EU stars,
Voyager probe, cyclone spiral) is drawn from geometric shapes in code.
The PNG encoder is pure stdlib too (`zlib` + `struct`, RGB, no interlace).

Running the program twice produces byte-identical PNG output: there is no
randomness and no timestamp anywhere in the image or the file.

## How to run

```sh
python3 main.py
```

The image is written to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output` when the variable is not set).

## The stories covered

1. **GTA VI rolls out worldwide** — After 13 years of waiting, Grand Theft
   Auto VI begins its global rollout. Players return to Vice City.
2. **Jeffries nominated as Speaker** — Democrats nominate Hakeem Jeffries
   as Speaker of the House. He would be the first African-American
   Speaker.
3. **US and Iran strike again** — US and Iran strike each other again.
   Iran hits Bahrain and Kuwait; the US strikes missile sites on Qeshm
   Island.
4. **EU proposes 45bn loan for Ukraine** — The EU proposes a 45 billion
   euro loan for Ukraine, to be repaid once Russia pays reparations.
5. **Voyager 1 reaches one light-day** — NASA's Voyager 1 is believed to
   reach one light-day from Earth, nearly 50 years after launch.
6. **Cyclone Akvan nears India** — Cyclone Akvan nears India's east coast.
   It is expected to cross between Machilipatnam and Puri.

## Layout

- Teal masthead with the date set large: **THURSDAY, 19 NOVEMBER 2026**
- Lead story panel (GTA VI) with a drawn game-controller icon
- Four stories in a 2×2 grid, each with its own drawn icon
- Wide bottom row for the cyclone story
- Footer crediting reports published on 19 November 2026

## License

MIT — see `LICENSE`.
