# The World in One Page — Friday 20 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![make.fun rank](https://make.fun/badge/news-image-20261120/Joppy26/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![make.fun reward](https://make.fun/badge/news-image-20261120/Joppy26/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper-style broadsheet that sums up Friday 20 November 2026 in a single
1024x1024 image: the first Trump–Xi–Putin trilateral summit in Shenzhen, the
ICJ's 9-6 ruling that Myanmar committed genocide against the Rohingya, a fifth
straight day of falls for US stocks, and 33 more stories from six continents —
each one numbered on a schematic world map, with a market ticker at the foot
of the page.

## Rebuild it

```sh
python3 gen.py
```

That renders `entry.png` (1024x1024). The renderer is deterministic — no
network, no clock, no randomness — so running it twice produces byte-identical
output. `main.ts` copies `entry.png` to the output directory
(`MAKEFUN_OUTPUT_DIR`, or `/output`) and verifies the copy is byte-for-byte
identical.

## Verified rebuild facts

- `entry.png` is 1024x1024 and under 1 MiB.
- Two consecutive runs of `python3 gen.py` produce byte-identical output
  (same SHA-256).
- `node main.ts` with `MAKEFUN_OUTPUT_DIR` set copies `entry.png` to that
  directory byte-identically.

Built for the make.fun bounty
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).
