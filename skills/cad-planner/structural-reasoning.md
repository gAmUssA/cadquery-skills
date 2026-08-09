# Structural Reasoning for CAD Design

## Purpose
Load this knowledge when user requests involve: bracket, support, shelf, cantilever, column, tower, frame, beam, mount, stand, arm, overhang.

---

## Load Path Thinking

Before designing any load-bearing structure, visualize:

1. **Load entry point** — Where does force enter? (shelf surface, hook tip, bracket arm)
2. **Load path** — How does force travel through the structure?
3. **Ground/anchor point** — Where does force exit to mounting surface?

**Example: Shelf bracket**
- Load: Downward on shelf (books, items)
- Path: Shelf → bracket arm → corner joint → wall plate
- Critical: Maximum stress at wall junction (bending moment)

---

## Structural Strategies

### Cantilevers (shelves, arms, overhangs)

**Problem:** Bending stress concentrated at root

**Solutions:**
- Increase depth at root (taper from thick→thin toward tip)
- Add ribs on underside (tension side)
- Triangle gusset brace from wall
- Use I-beam or C-channel profile instead of solid rectangle

**Proportional rules:**
- Depth at root ≥ Length / 8 for minimal sag
- Add gusset if Length > 5× thickness
- Rib height = 3-5× base thickness

```python
# ❌ Weak cantilever (will sag)
result = cq.Workplane("XY").box(200, 50, 5)

# ✅ Strong cantilever (with gusset)
arm = cq.Workplane("XY").box(200, 50, 8)
gusset = (
    cq.Workplane("XZ")
    .moveTo(0, 0).lineTo(100, 0).lineTo(0, 40).close()
    .extrude(8)
)
result = arm.union(gusset).edges("|Y").fillet(3)
```

### Vertical Columns (supports, legs, towers)

**Problem:** Buckling under compression

**Stability rules:**
- Height / diameter < 15 → stable (stocky)
- Height / diameter > 25 → will buckle (slender)
- Add cross-bracing every 5× diameter in height

**Solutions:**
- Hollow tube stronger than solid for same weight
- Widen base (pyramid/cone taper)
- Connect multiple columns with cross-braces
- Use triangulated frame (truss)

```python
# ❌ Slender column (will buckle)
result = cq.Workplane("XY").cylinder(300, 8)  # ratio = 37

# ✅ Stable column (tapered base)
result = cq.Workplane("XY").cone(15, 8, 300)  # wider at bottom
```

### Joints and Corners

**Problem:** Stress concentration at sharp internal corners

**Golden rule:** ALWAYS fillet internal corners for stress relief

**Solutions:**
- Internal fillet radius ≥ 2mm (preferably 3-5mm)
- Add gusset plates at T-joints and L-joints
- Distribute load over area, not point contact
- Overlap joints ≥ 3× material thickness

```python
# ❌ Stress concentration (will crack at corner)
wall = cq.Workplane("XY").box(100, 5, 50)
rib = cq.Workplane("YZ").box(5, 50, 30).translate((0, 0, -25))
result = wall.union(rib)

# ✅ Stress relief (filleted internal corners)
wall = cq.Workplane("XY").box(100, 5, 50)
rib = cq.Workplane("YZ").box(5, 50, 30).translate((0, 0, -25))
result = wall.union(rib).edges("|X").fillet(3)
```

### Flat Panels Under Load

**Problem:** Thin panels flex and buckle

**Solutions:**
- Add ribbing pattern: grid, radial, or honeycomb
- Rib depth = 3-5× panel thickness
- Rib spacing = 20-50× panel thickness
- Add perimeter frame (picture frame effect)

**Rib spacing guide:**
| Panel Thickness | Max Unsupported Span | Rib Spacing |
|-----------------|---------------------|-------------|
| 2mm | 50mm | 40mm |
| 3mm | 75mm | 60mm |
| 5mm | 125mm | 100mm |

---

## Quick Stability Checks

### Will it tip over?
- Base width ≥ 1.5× height for static stability
- Base width ≥ 2.5× height if it moves or gets bumped

### Will it sag?
- Cantilever: Depth at root ≥ Length / 8
- Supported beam: Depth ≥ Span / 15

### Will the column buckle?
- Slenderness ratio = Height / (smallest dimension)
- Safe if < 15, risky if > 25

---

## Common Structural Patterns

### Triangulation (strongest shape)
Triangles don't deform under load—use for maximum rigidity.

```python
# Triangle gusset at corner
gusset = (
    cq.Workplane("XZ")
    .moveTo(0, 0).lineTo(40, 0).lineTo(0, 40).close()
    .extrude(5)
)
```

### Ribbing (panel reinforcement)
```python
# Grid ribs on flat panel
panel = cq.Workplane("XY").box(100, 100, 3)
rib_x = cq.Workplane("XZ").center(0, 1.5).rect(100, 10).extrude(3)
rib_y = cq.Workplane("YZ").center(0, 1.5).rect(100, 10).extrude(3)
result = panel.union(rib_x).union(rib_y)
```

### Box Section (torsion resistance)
Closed tubes resist twisting far better than open channels.

```python
# Hollow rectangular tube
result = cq.Workplane("XY").rect(40, 20).extrude(100).shell(-3)
```

### I-Beam Profile (bending efficiency)
Material at top and bottom, minimal in middle—optimized for bending.

```python
# Simple I-beam profile
i_beam = (
    cq.Workplane("XY")
    .rect(40, 5).extrude(100)  # top flange
    .faces("<Z").workplane().rect(5, 30).extrude(-100)  # web
    .faces("<Z").workplane().rect(40, 5).extrude(-100)  # bottom flange
)
```

---

## Material Impact on Structure

| Material | Key Consideration |
|----------|-------------------|
| **PLA (3D print)** | Weak in tension, needs thick walls (3mm+), generous fillets |
| **ABS** | Slightly stronger than PLA, same reinforcement strategy |
| **Aluminum** | Strong but fillet corners (fatigue cracks), can use thinner walls |
| **Steel** | High strength but heavy, optimize with hollow sections |
| **Acrylic/PC** | Brittle—MUST fillet all internal corners, avoid point loads |
| **Wood** | Strong along grain, weak across—orient grain along load path |

---

## Architect's Perspective

Think like someone designing buildings:

1. **Foundation first** — Wide, stable base that distributes load to ground
2. **Columns for compression** — Vertical members carry weight down
3. **Beams for spanning** — Horizontal members bridge gaps
4. **Bracing for stability** — Diagonal members prevent racking/collapse
5. **Symmetry for balance** — Centered loads prevent tipping moments

**Cathedral principle:** The flying buttresses exist because the walls alone can't handle the outward thrust of the roof. Every force needs a reaction path.
