---
name: design-versioning
description: Track CAD design iterations with Git - commit changes, compare versions, maintain history like code.
---

# Design Versioning Skill

## Description
Track design iterations using Git version control. Treat CAD designs like code - commit changes, compare versions, and maintain history.

## Instructions

Help users version their 3D designs using Git. CAD files are code, and should be treated with the same rigor as software.

### Core Concepts

**Why version CAD designs?**
- Track every design iteration
- Compare changes between versions
- Revert to previous designs
- Collaborate with team members
- Document design decisions

### Git Workflow for CAD

#### Save a Design Version
```bash
# Stage the design file
git add design.py

# Commit with descriptive message
git commit -m "Add motor mount bracket with NEMA 17 hole pattern"
```

#### Version Naming Conventions
Use semantic versioning for major milestones:
```bash
git tag v1.0.0 -m "Initial design - basic bracket"
git tag v1.1.0 -m "Added mounting holes"
git tag v2.0.0 -m "Complete redesign with ribbing"
```

#### View Design History
```bash
# See all commits
git log --oneline

# See changes in a specific commit
git show <commit-hash>

# Compare two versions
git diff v1.0.0 v2.0.0 design.py
```

#### Restore Previous Version
```bash
# View old version without changing current
git show v1.0.0:design.py

# Restore to previous version
git checkout v1.0.0 -- design.py
```

### Recommended .gitignore
```gitignore
# Generated exports (regenerate from code)
exports/*.step
exports/*.stl
exports/*.gltf
exports/*.glb

# Temporary files
*.pyc
__pycache__/
.cadquery_cache/

# IDE files
.vscode/settings.json
*.code-workspace

# OS files
.DS_Store
Thumbs.db
```

### Commit Message Guidelines

**Format:**
```
<type>: <short description>

[optional body with details]
```

**Types:**
- `feat:` New feature or component
- `fix:` Bug fix or correction
- `refactor:` Code reorganization
- `dims:` Dimension changes
- `style:` Appearance changes (color, etc.)
- `docs:` Documentation updates

**Examples:**
```bash
git commit -m "feat: Add mounting flange with 4x M4 holes"
git commit -m "dims: Increase wall thickness from 3mm to 5mm"
git commit -m "fix: Correct hole spacing to match NEMA 17 spec"
git commit -m "refactor: Extract common parameters to top of file"
```

### Branch Strategy for Complex Designs

```bash
# Main branch: production-ready designs
main

# Feature branches for experiments
git checkout -b feature/add-cooling-fins
git checkout -b experiment/honeycomb-infill

# Merge when ready
git checkout main
git merge feature/add-cooling-fins
```

### Comparing Design Changes

Since CadQuery files are Python code, you can:
1. Use `git diff` to see parameter changes
2. Generate both versions and visually compare in preview
3. Use comments to document why changes were made

```python
# v1.0: Original design
# wall_thickness = 3  # Too thin, cracked during testing

# v1.1: Increased thickness per stress analysis
wall_thickness = 5  # Passed 50N load test
```

### Design Review Checklist
Before committing, verify:
- [ ] Code generates without errors
- [ ] Preview looks correct
- [ ] Parameters are clearly named
- [ ] Comments explain design intent
- [ ] Commit message is descriptive

## Output Format
When user asks about versioning, provide the appropriate Git commands and explain the workflow.
