"""Check a generated pencil holder model against the skill smoke test."""

import argparse
import math
import runpy
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import cadquery as cq


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


def check_stl(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 84:
        raise AssertionError("STL export is too short for binary STL")
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    if triangle_count == 0 or len(data) != 84 + 50 * triangle_count:
        raise AssertionError("STL export has invalid binary triangle data")

    points = []
    volume = 0.0
    for triangle in struct.iter_unpack("<12fH", data[84:]):
        a, b, c = triangle[3:6], triangle[6:9], triangle[9:12]
        points.extend((a, b, c))
        volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            + a[1] * (b[2] * c[0] - b[0] * c[2])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6

    for axis, low, high in ((0, -40, 40), (1, -40, 40), (2, 0, 100)):
        values = [point[axis] for point in points]
        if not math.isclose(min(values), low, abs_tol=0.1) or not math.isclose(
            max(values), high, abs_tol=0.1
        ):
            raise AssertionError("STL export has incorrect placement or dimensions")

    expected_volume = math.pi * (40**2 * 100 - 37**2 * 96)
    if not math.isclose(abs(volume), expected_volume, rel_tol=0.01):
        raise AssertionError("STL export has incorrect mesh volume")
    for z in (4, 100):
        if not any(
            math.isclose(point[2], z, abs_tol=0.1)
            and math.isclose(math.hypot(point[0], point[1]), 37, abs_tol=0.1)
            for point in points
        ):
            raise AssertionError("STL export is missing the inner wall or base edge")


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

        check_stl(Path(output_dir) / "pencil_holder.stl")

    print("PASS: valid open pencil holder, 80 × 80 × 100 mm, 3 mm wall, 4 mm base, STL and STEP")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="Generated pencil_holder.py")
    args = parser.parse_args()
    check(args.model.resolve())
