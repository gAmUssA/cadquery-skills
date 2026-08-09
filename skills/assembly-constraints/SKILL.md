---
name: assembly-constraints
description: Create and manage CadQuery assemblies with parts, sub-assemblies, and constraint-based positioning.
---

# Assembly Constraints Skill

## Description
Create and manage CadQuery assemblies with parts, sub-assemblies, and constraint-based positioning.

## Instructions

You are a CadQuery assembly expert. Help users build modular, multi-part designs with proper constraints.

### Assembly Structure

```python
import cadquery as cq

def build():
    """Assembly description."""
    assy = cq.Assembly(name="assembly_name")
    
    # Add parts
    assy.add(part1, name="part1", color=cq.Color(0.7, 0.7, 0.7))
    assy.add(part2, name="part2", color=cq.Color(0.2, 0.6, 0.9))
    
    # Define constraints
    assy.constrain("part1?face_tag", "part2?face_tag", "Plane")
    
    # Solve
    assy.solve()
    
    return assy

result = build()
```

### Critical Rules

1. **Name all parts** - `assy.add(part, name="unique_name")` for navigation
2. **Tag mate faces** - Use `.tag("name")` on faces in part definitions
3. **Solve after constraints** - Always call `assy.solve()` before export
4. **Use config for shared params** - Import from `config.py`

### Constraint Types

| Type | Use Case | Example |
|------|----------|---------|
| **Plane** | Faces touch and align | Bolt head on plate |
| **Axis** | Centerlines align | Shaft in hole |
| **Point** | Centers coincide | Ball joint |
| **PointInPlane** | Point slides on surface | Slider |
| **Fixed** | Lock in place | Base plate |

### Constraint Syntax

```python
# Using tagged faces (preferred)
assy.constrain("part1?top", "part2?bottom", "Plane")

# Using face selectors
assy.constrain("part1@faces@>Z", "part2@faces@<Z", "Plane")

# With parameter (e.g., axis direction: 0=same, 180=opposite)
assy.constrain("part1@faces@>Z", "part2@faces@<Z", "Axis", param=0)

# Fixed position
assy.constrain("base", "Fixed")
```

### Sub-Assembly Access

```python
# Access nested parts with "/" separator
assy.constrain("subassy1/part1?top", "subassy2/part2?bottom", "Plane")
```

### Tagging Faces in Parts

```python
def build():
    part = (
        cq.Workplane("XY")
        .box(100, 50, 20)
    )
    
    # Tag faces for assembly references
    part.faces(">Z").tag("top")
    part.faces("<Z").tag("bottom")
    part.faces(">X").tag("side_right")
    part.faces("<X").tag("side_left")
    part.faces(">Y").tag("front")
    part.faces("<Y").tag("back")
    
    return part
```

### Face Selectors Reference

| Selector | Meaning |
|----------|---------|
| `>Z` | Highest Z face (top) |
| `<Z` | Lowest Z face (bottom) |
| `>X` | Highest X face (right) |
| `<X` | Lowest X face (left) |
| `>Y` | Highest Y face (front) |
| `<Y` | Lowest Y face (back) |
| `\|Z` | Faces perpendicular to Z |
| `#Z` | Faces parallel to Z |

### Positioning with Location

```python
# Initial position (helps solver converge)
assy.add(part, name="part1", loc=cq.Location((x, y, z)))

# Position with rotation (axis, angle in degrees)
assy.add(part, name="part2", loc=cq.Location((0, 0, 50), (1, 0, 0), 90))
```

### Color Assignment

```python
# Named colors
assy.add(part, name="p1", color=cq.Color("red"))
assy.add(part, name="p2", color=cq.Color("steelblue"))

# RGB (0-1 range)
assy.add(part, name="p3", color=cq.Color(0.7, 0.7, 0.7))

# RGBA with transparency
assy.add(part, name="p4", color=cq.Color(0.2, 0.6, 0.9, 0.5))
```

### Importing Parts from Files

```python
# From parts folder
from parts.bracket import build as make_bracket
from parts.link import build as make_link

# From vendor STEP files
motor = cq.importers.importStep("vendor_parts/motor.step")

assy = cq.Assembly()
assy.add(make_bracket(), name="bracket")
assy.add(make_link(length=80), name="link")
assy.add(motor, name="motor", color=cq.Color("darkgray"))
```

### Export Assembly

```python
assy.solve()

# STEP (preserves part structure)
assy.save("assembly.step")

# GLTF for web viewing
assy.save("assembly.gltf")

# Fused single solid
assy.save("assembly.step", mode="fused")
```

### Example: Simple Bracket Assembly

```python
import cadquery as cq

def make_plate():
    plate = cq.Workplane("XY").box(100, 50, 5)
    plate.faces(">Z").tag("top")
    plate.faces("<Z").tag("bottom")
    return plate

def make_standoff(height=20):
    standoff = cq.Workplane("XY").cylinder(height, 5)
    standoff.faces("<Z").tag("base")
    standoff.faces(">Z").tag("top")
    return standoff

def build():
    assy = cq.Assembly(name="bracket_assy")
    
    # Add base plate
    assy.add(make_plate(), name="plate", color=cq.Color(0.8, 0.8, 0.8))
    
    # Add 4 standoffs
    positions = [(-40, -20), (40, -20), (-40, 20), (40, 20)]
    for i, (x, y) in enumerate(positions):
        assy.add(
            make_standoff(), 
            name=f"standoff_{i}", 
            color=cq.Color(0.3, 0.3, 0.3),
            loc=cq.Location((x, y, 5))  # On top of plate
        )
        assy.constrain(f"standoff_{i}?base", "plate?top", "Point")
    
    assy.solve()
    return assy

result = build()
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Solver fails | Set initial `loc=` positions closer to final |
| Parts overlap | Check constraint directions (Axis param) |
| Face not found | Verify tag exists, check selector syntax |
| Import error | Check file path, use absolute if needed |

---

## Selection Context in Assemblies (viewer-integrated environments only)

In hosts with a 3D viewer integration, clicking a part sends selection context
(part name, bounding box). Without a viewer the user refers to parts by their
assembly `name=` — the workflow below is identical either way:

### Modifying Selected Assembly Parts

1. **Identify by name** - Match selection to named part in assembly
2. **Modify the part builder** - Change the function that creates that part
3. **Keep other parts** - Don't alter unrelated geometry

### Example: User selects "standoff_0" and says "make this taller"
```python
# BEFORE
def make_standoff(height=20):
    standoff = cq.Workplane("XY").cylinder(height, 5)
    # ...

# User selects standoff_0 (height ~20mm)
# User says: "make this 30mm tall"

# AFTER - only height parameter changed
def make_standoff(height=30):  # Changed from 20 to 30
    standoff = cq.Workplane("XY").cylinder(height, 5)
    # ...
```

### Removing Parts from Assembly
```python
# BEFORE
assy.add(make_plate(), name="plate")
assy.add(make_standoff(), name="standoff_0")  # User selected this
assy.add(make_standoff(), name="standoff_1")

# User says: "delete this" (standoff_0 selected)

# AFTER - remove the selected part and its constraints
assy.add(make_plate(), name="plate")
# standoff_0 removed entirely
assy.add(make_standoff(), name="standoff_1")
```

