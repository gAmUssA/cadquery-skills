# Pencil holder skill smoke test

Run this prompt in a fresh Codex or Claude Code session with the installed
`cad-code-generation` skill:

> Create a parametric pencil holder: a round upright cup, 80 mm outside
> diameter, 100 mm tall, 3 mm wall, 4 mm solid base, open at the top. Put its
> base on Z=0, center it on the Z axis, define `build()` returning the CadQuery
> solid, and export both STL and STEP in the main block. Return complete Python
> code.

Save the generated code as `pencil_holder.py`, then run the checker from the
repository root:

```bash
uv run --no-project --python 3.12 --with cadquery python tests/pencil-holder/check.py /path/to/pencil_holder.py
```

The checker runs the generated script in a temporary directory and verifies
the single solid, dimensions, wall, base, open cavity, and both exports. Its
temporary STL and STEP files are discarded after the run.
