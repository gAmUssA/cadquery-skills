# cadquery-skills

Codex and Claude Code skills for parametric code-CAD with [CadQuery](https://cadquery.readthedocs.io/).
Adapted for standalone use from the skills in
[shdaifat/cadquery-cad-vscode](https://github.com/shdaifat/cadquery-cad-vscode) (MIT).

| Skill | What it does |
|---|---|
| **cad-planner** | "Chief Engineer" persona: analyzes requirements, decomposes machines into assemblies/parts (filesystem = architecture), confidence-driven assumptions instead of question loops |
| **cad-code-generation** | Parametric CadQuery code generation rules, with a pattern library (brackets, gears, enclosures…) and aesthetics guidance |
| **assembly-constraints** | Multi-part `cq.Assembly` builds with constraint-based positioning (mates, tags, sub-assemblies) |
| **cadquery-export** | Choosing and generating exports: STL, STEP, AMF, 3MF, DXF, SVG — tolerances, units, manufacturing targets |
| **design-versioning** | Git workflow for CAD-as-code: commit conventions, comparing design iterations, tagging prints |

## Install

### Codex

The repository contains a portable `plugin.json` and five skills under `skills/`.
Add this GitHub repository as a marketplace, then install the plugin:

```bash
codex plugin marketplace add gAmUssA/cadquery-skills
codex plugin add cadquery-skills@cadquery-skills
```

For a project-local install without the plugin browser, copy the skill folders
to the project's `.agents/skills/` directory:

```bash
mkdir -p your-project/.agents/skills
cp -R skills/* your-project/.agents/skills/
```

Start a new Codex session in the project. Invoke a skill as `$cad-planner`,
`$cad-code-generation`, and so on, or describe a CAD task for automatic skill
selection.

### Claude Code

**As a plugin** (updates with `git pull`):

```
/plugin marketplace add gAmUssA/cadquery-skills
/plugin install cadquery-skills@cadquery-skills
```

**Or copy into a project** — drop the five folders from `skills/` into your
project's `.claude/skills/`:

```bash
cp -R skills/* your-project/.claude/skills/
```

Then invoke with `/cad-planner`, `/cad-code-generation`, etc., or describe a CAD
task and let skill matching pick them up.

## Requirements

- A Python environment with `cadquery` installed (Python 3.12 recommended —
  CadQuery's OCP wheels lag the newest Python). `uv add cadquery` or
  `pip install cadquery`.
- No GUI required: the skills target headless scripts that export STL/STEP.
  `show_object()` guidance applies only inside cq-editor.

## Smoke test

The [pencil holder test](tests/pencil-holder/PROMPT.md) checks a model generated
by either host for its open cavity, wall and base dimensions, and STL/STEP
exports.

## Changes from the original

The originals were written for a VS Code extension with a live 3D viewer and
scaffolding commands. This adaptation makes them host-agnostic:

- `/scaffold`, `/new-project`, `/new-assembly` extension commands → the agent
  creates folders/stub files directly with its file tools
- Viewer selection-context sections marked as conditional (used only when the
  host provides them)
- `result`-variable auto-rendering → explicit `cq.exporters.export()` guidance
  for standalone scripts
- Added YAML frontmatter (`name`/`description`) for skill discovery

## License

MIT — original skills © shdaifat, adaptation © Viktor Gamov. See [LICENSE](LICENSE).
