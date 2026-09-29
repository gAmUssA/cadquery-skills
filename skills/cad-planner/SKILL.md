---
name: cad-planner
description: Plan a parametric CadQuery part or machine, including requirements, manufacturability, assembly boundaries, and a practical implementation path.
---

# CAD Planner

Process steps in order. Do not skip ahead.

## Step 1 — Assess the Design

Extract the requested function, geometry, dimensions, material, manufacturing
method, loads, interfaces, and constraints. Identify missing information that
would change the geometry or make the design unsafe. Use documented assumptions
for ordinary gaps; ask a focused question when a critical dimension or interface
cannot reasonably be inferred.

Check scale, fit, likely load paths, wall thickness, clearances, tolerances, and
whether the proposed features can be manufactured by the chosen process. State
the main assumptions and any material limitation in a short design summary.
For structural patterns, read [structural-reasoning.md](structural-reasoning.md)
when the request involves load-bearing parts.

Proceed immediately to Step 2.

## Step 2 — Decompose the Model

For a single part, keep dimensions as parameters and plan one model file. For a
machine, divide it into parts and assemblies with clear mating interfaces. Use
folders for assemblies when that makes the project easier to build and inspect;
each assembly folder should have an `assembly.py` with a `build()` function.
Prefer standard hardware where its dimensions and availability fit the design.

Show a compact file tree for a multi-part design. Explain the key interface and
positioning decisions. Proceed immediately to Step 3.

## Step 3 — Implement the Useful Slice

If the user asked for a design or working CAD project, create the necessary
folders and runnable CadQuery files using the available file tools. Start with a
meaningful part and its assembly connection. Create referenced files before
importing them. Record assumptions as parameters or nearby comments.

Run the model and inspect the generated geometry or export when the environment
has CadQuery. If execution is unavailable, report the specific missing
prerequisite. Give the user the design summary, files created, and verification
result. Finish here.
