---
name: cad-code-generation
description: Create or edit runnable parametric CadQuery Python models for parts and assemblies from a CAD request.
---

# CAD Code Generation

Process steps in order. Do not skip ahead.

## Step 1 — Read the Model Context

Inspect the target file and related parts before editing. If the user names a
part or file, use it. If a host supplies 3D viewer selection data, use the
selected part and coordinates as additional context. Otherwise use the user's
written description. For a new standalone part, use a descriptive Python file
name in the existing project structure.

Identify existing features and parameters to preserve. Use millimeters unless
the project specifies another unit. For dimensions that affect fit or function,
ask when they cannot be inferred; otherwise state reasonable assumptions.
Proceed immediately to Step 2.

## Step 2 — Build the Geometry

Write complete, runnable Python with all imports and defined variables. Keep
dimensions as named parameters. Assign the final `cq.Workplane`, `cq.Shape`, or
`cq.Assembly` to `result` at module level when the project or viewer expects it.
For ordinary standalone scripts, expose a `build()` function and export the
result explicitly from a main block. Do not use `show_object()` outside
cq-editor or another host that defines it.

When editing a model, preserve existing features unless the user asks to
remove or change them. Check that holes, shells, chamfers, and fillets fit their
parent geometry. Build assemblies from named parts with explicit positions or
constraints. Refer to [pattern-library.md](pattern-library.md) for mounting,
joining, and other reusable geometry patterns. Read [aesthetics.md](aesthetics.md)
when appearance matters.

Proceed immediately to Step 3.

## Step 3 — Verify the Result

Run the script using the project's CadQuery environment and check the generated
solid or export. Inspect a rendered preview when a viewer is available. Report
the file changed, assumptions, and the command and result used to verify it.
When CadQuery is unavailable, say which runtime prerequisite is missing.
Finish here.
