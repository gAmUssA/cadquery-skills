"""Check a generated pencil holder model against the skill smoke test."""

import argparse
import math
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

import cadquery as cq
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape


def single_solid(model: cq.Workplane | cq.Shape) -> cq.Shape:
    if isinstance(model, cq.Workplane):
        solids = model.solids().vals()
    elif isinstance(model, cq.Shape):
        solids = model.Solids()
    else:
        raise AssertionError("build() must return a CadQuery shape or workplane")
    if len(solids) != 1 or not solids[0].isValid():
        raise AssertionError("Model must contain one valid solid")
    return solids[0]


def check_geometry(shape: cq.Shape) -> None:
    bounds = shape.BoundingBox()
    for actual, expected, label in (
        (bounds.xlen, 80, "outside diameter X"),
        (bounds.ylen, 80, "outside diameter Y"),
        (bounds.zlen, 100, "height"),
        (bounds.xmin, -40, "centered X"),
        (bounds.ymin, -40, "centered Y"),
        (bounds.zmin, 0, "base Z"),
    ):
        if not math.isclose(actual, expected, abs_tol=0.01):
            raise AssertionError(f"{label}: expected {expected} mm, got {actual:.3f} mm")

    expected_volume = math.pi * (40**2 * 100 - 37**2 * 96)
    if not math.isclose(shape.Volume(), expected_volume, abs_tol=1):
        raise AssertionError(
            f"Expected 3 mm wall and 4 mm base volume {expected_volume:.3f} mm³, "
            f"got {shape.Volume():.3f} mm³"
        )

    for point, expected, label in (
        ((0, 0, 2), True, "solid base"),
        ((0, 0, 5), False, "cavity above 4 mm base"),
        ((0, 0, 99), False, "open top"),
        ((36, 0, 50), False, "37 mm inner radius"),
        ((38, 0, 50), True, "3 mm wall"),
    ):
        if shape.isInside(cq.Vector(*point)) != expected:
            raise AssertionError(f"Unexpected material at {point}: {label}")


def check(model_path: Path) -> None:
    namespace = runpy.run_path(str(model_path))
    build = namespace.get("build")
    if not callable(build):
        raise AssertionError("Model must define a callable build()")

    check_geometry(single_solid(build()))

    with tempfile.TemporaryDirectory() as output_dir:
        subprocess.run([sys.executable, str(model_path)], cwd=output_dir, check=True)
        for name in ("pencil_holder.stl", "pencil_holder.step"):
            path = Path(output_dir) / name
            if not path.is_file() or path.stat().st_size == 0:
                raise AssertionError(f"Missing or empty export: {name}")
        imported = cq.importers.importStep(str(Path(output_dir) / "pencil_holder.step"))
        check_geometry(single_solid(imported))

        stl_shape = TopoDS_Shape()
        if not StlAPI_Reader().Read(stl_shape, str(Path(output_dir) / "pencil_holder.stl")):
            raise AssertionError("STL export could not be read")
        stl = cq.Shape.cast(stl_shape)
        stl_bounds = stl.BoundingBox()
        if len(stl.Faces()) == 0 or any(
            not math.isclose(actual, expected, abs_tol=0.1)
            for actual, expected in (
                (stl_bounds.xlen, 80),
                (stl_bounds.ylen, 80),
                (stl_bounds.zlen, 100),
            )
        ):
            raise AssertionError("STL export has missing faces or incorrect dimensions")

    print("PASS: valid open pencil holder, 80 × 80 × 100 mm, 3 mm wall, 4 mm base, STL and STEP")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Generated pencil_holder.py")
    args = parser.parse_args()
    check(args.model.resolve())
