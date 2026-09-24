[中文](README.md) | English

# Xiaoma Painting · MLP G4 Skill

A rule pack for AI-drawn *My Little Pony* G4 (Friendship is Magic) fan art, usable as a Codex / ChatGPT Skill.

It targets three recurring failures: broken anatomy (extra legs, front hooves drawn as human hands, wings sprouting from the ribs), broken character identity (body color, mane color or cutie mark replaced), and non-reproducible process (every generation uses different steps, styles and acceptance criteria).

## Installation

1. Download the latest `小马绘画_vX.Y_覆盖安装版.zip` from [Releases](../../releases).
2. Extract it into your Codex skills directory: `%USERPROFILE%\.codex\skills\` on Windows, `~/.codex/skills/` elsewhere.
3. Verify the path reads `.../skills/mlp-g4-official-style/SKILL.md`.

To upgrade, download the new zip and overwrite the same folder; no need to delete the old one first.

## Layered structure

Rules are organized in four layers with no sentence duplicated across them, loaded on demand:

| Layer | Content | Location |
|---|---|---|
| L0 | Pony anatomy: proportions, legs and front hooves, pegasus wings, cutie mark, identity constants, P0 criteria | `references/body-base.md` |
| L1 | Drawing process: composition, skeleton, volumes, structural gate, line art and lighting, detail, review | `references/drawing-process.md` |
| L2 | Style modules: official G4 (default), Dunhuang flying apsara | `references/styles/` |
| L3 | Character library: 8 characters, each with per-style sub-entries | `references/characters/` |

A separate acceptance priority scale applies: **P0** anatomy, **P1** character identity and style, **P2** lighting and decoration. A P0 failure can never be compensated by style or lighting.

## Layout

```text
mlp-g4-official-style/
├── SKILL.md                        Entry: priorities, layer routing, style isolation, pre-flight checks
├── CHANGELOG.md                    Versioned change log
├── agents/openai.yaml              UI metadata and invocation policy
├── assets/icon.svg
└── references/
    ├── body-base.md                L0
    ├── drawing-process.md          L1
    ├── styles/
    │   ├── g4-official.md          L2 default style
    │   └── dunhuang-feitian.md     L2 Dunhuang style
    └── characters/
        ├── _template.md            Template for new characters
        └── ...                     8 characters (Fluttershy, Rainbow Dash, Twilight Sparkle, Rarity, Applejack, Pinkie Pie, Princess Celestia, Princess Luna)
```

## Usage

After installation, just describe the request; the skill is picked up automatically. You can also invoke it explicitly:

```text
Use $mlp-g4-official-style: Rainbow Dash looking back, Dunhuang flying apsara style
```

Every generation ends with a fixed four-line self-check (counts, identity, structure, verdict). If the structure fails, it returns REJECTED and rolls back instead of piling detail onto a broken image.

## Extending

- **New character**: copy `references/characters/_template.md` and fill in identity constants and common mistakes; `SKILL.md` needs no change.
- **New style**: add one file under `references/styles/` describing only that style's line work, palette, materials and mood. Style modules stay isolated; no mixing, and never overriding the L0 anatomy rules.
- **Rule changes**: anatomy lives only in L0, process only in L1 — one sentence appears in exactly one file.

## Versioning

Release flow: bump the version in `CHANGELOG.md` → build the zip → publish a Release with the zip as asset → delete the local zip. See [Releases](../../releases) for history.
