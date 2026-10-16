# Reaction sticker skill

Give this repo to Codex or Claude to make sourced, static reaction stickers with transparent backgrounds and white outlines.

<img src="examples/woman-yelling-at-cat.png" alt="Woman yelling and pointing at a cat, cut out as a sticker with a white outline" width="420">

Install in a project:

```bash
git clone https://github.com/CouldNot/create-reaction-sticker-skill.git .agents/skills/reaction-sticker-pack
```

For Claude Code, also link it into its skills directory:

```bash
mkdir -p .claude/skills
ln -s ../../.agents/skills/reaction-sticker-pack .claude/skills/reaction-sticker-pack
```

Start a new agent session and say: **“Use the reaction-sticker-pack skill to make 30 modern reaction stickers.”**
