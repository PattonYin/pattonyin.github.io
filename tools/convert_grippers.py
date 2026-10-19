"""Build the website grippers without copying source CAD into the repository.

Usage: python tools/convert_grippers.py /path/to/kiwi_robot_share
Requires trimesh, fast-simplification, numpy and scipy. Run after convert_robots.py.
"""

import argparse
import copy
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

import numpy as np
import trimesh
from scipy.optimize import least_squares

from convert_robots import collect_defaults, resolve, transform, walk_bodies

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/robots"
CACHE = ROOT / ".preview/robotiq-source"
REVISION = "71f066ad0be9cd271f7ed58c030243ef157af9f4"
RAW = f"https://raw.githubusercontent.com/google-deepmind/mujoco_menagerie/{REVISION}/robotiq_2f85"
FACE_BUDGET = 6000


def download(name):
    path = CACHE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    # Cache the pinned revision separately from any exploratory downloads.
    path = path.with_name(REVISION[:8] + "-" + path.name)
    if not path.exists():
        path.write_bytes(urllib.request.urlopen(f"{RAW}/{name}", timeout=45).read())
    return path


def compact(mesh, face_budget=FACE_BUDGET):
    if mesh.visual.kind in ("vertex", "face"):
        # The camera GLB uses five vertex colours in one mesh. Simplify each
        # colour region separately so decimation keeps its board/lens colours.
        colors, labels = np.unique(mesh.visual.face_colors, axis=0, return_inverse=True)
        parts = []
        for index, color in enumerate(colors):
            part = mesh.submesh([np.flatnonzero(labels == index)], append=True)
            budget = max(100, round(face_budget * len(part.faces) / len(mesh.faces)))
            if len(part.faces) > budget:
                part = part.simplify_quadric_decimation(face_count=budget)
            part.visual = trimesh.visual.ColorVisuals(mesh=part, face_colors=color)
            parts.append(part)
        return trimesh.util.concatenate(parts)
    material = copy.deepcopy(mesh.visual.material) if hasattr(mesh.visual, "material") else None
    if len(mesh.faces) > face_budget:
        mesh = mesh.simplify_quadric_decimation(face_count=face_budget)
    if material is not None:
        mesh.visual = trimesh.visual.TextureVisuals(material=material)
    return mesh


def colored(mesh, rgba):
    mesh.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.15, roughnessFactor=0.55))
    return mesh


def save_scene(scene, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(scene.export(file_type="glb"))
    print(f"{path.relative_to(ROOT)}: {path.stat().st_size / 1024:.1f} KiB", flush=True)


def attach(robot, links, flange, gripper):
    path = OUT / robot / "kinematics.json"
    kin = json.loads(path.read_text())
    # The arm ends at link7; replace any existing tool (also makes reruns safe).
    kin["links"] = kin["links"][:8]
    for link in links:
        link = copy.deepcopy(link)
        if link["parent"] == -1:
            link["parent"] = 7
            link["pos"] = (np.array(link["pos"]) + flange).tolist()
        else:
            link["parent"] += 8
        kin["links"].append(link)
    kin["gripper"] = gripper
    path.write_text(json.dumps(kin, indent=1) + "\n")


def robotiq():
    root = ET.parse(download("2f85.xml")).getroot()
    materials, classes = collect_defaults(root)
    links = []
    walk_bodies(root.find("worldbody/body"), -1, links, materials, classes)
    bodies = {body.get("name"): body for body in root.iter("body")}
    exported = {}
    for link in links:
        joint = bodies[link["name"]].find("joint")
        if joint is not None:
            attrs = resolve(joint, "joint", classes, "2f85")
            if "pos" in attrs:
                link["joint"]["pos"] = list(map(float, attrs["pos"].split()))
        geoms = link.pop("geoms")
        key = tuple((g["mesh"], tuple(g["rgba"])) for g in geoms)
        if key not in exported:
            scene = trimesh.Scene()
            for i, geom in enumerate(geoms):
                mesh = compact(trimesh.load(download(f"assets/{geom['mesh']}.stl"), force="mesh"))
                mesh.apply_scale(0.001)  # MJCF 2f85 mesh default: millimetres.
                mesh.apply_transform(transform(geom["pos"], geom["quat"]))
                scene.add_geometry(colored(mesh, geom["rgba"]), node_name=f"part{i}")
            name = f"{link['name']}.glb"
            save_scene(scene, OUT / "robotiq-2f85" / name)
            exported[key] = f"../robotiq-2f85/{name}"
        link["mesh"] = exported[key]

    # Solve the source MJCF closed linkage with the coupler at its open stop. In particular,
    # the follower hinge has an offset pivot; simply mirroring driver angles
    # would pull its pins apart. Store samples for lightweight browser playback.
    def rotate(angle, point):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s], [s, c]]) @ point

    driver_origin = np.array([0.0306011, 0.054904])
    coupler_origin = np.array([0.0315, -0.0041])
    spring_origin = np.array([0.0132, 0.0609])
    follower_origin = np.array([0.055, 0.0375])
    pivot = np.array([-0.018, 0.0065])
    anchor = spring_origin + follower_origin - driver_origin - coupler_origin
    samples = []
    previous = [0, 0]
    for driver in np.linspace(0, 0.799, 65):
        def residual(q):
            spring, follower = q
            follower_pin = spring_origin + rotate(spring, follower_origin + pivot) - rotate(spring + follower, pivot)
            coupler_pin = driver_origin + rotate(driver, coupler_origin + anchor)
            return follower_pin - coupler_pin
        solved = least_squares(residual, previous, xtol=1e-13, ftol=1e-13, gtol=1e-13)
        assert np.linalg.norm(residual(solved.x)) < 1e-8
        spring, follower = solved.x
        previous = solved.x
        samples.append([driver, 0, spring, follower])
    motion = {}
    for side in ("left", "right"):
        for i, part in enumerate(("driver", "coupler", "spring_link", "follower")):
            motion[f"{side}_{part}_joint"] = [round(row[i], 8) for row in reversed(samples)]
    attach("panda", links, [0, 0, 0.107], {"open": 0.04, "joints": motion})
    (OUT / "robotiq-2f85/LICENSE").write_bytes(download("LICENSE").read_bytes())
    for name in ("hand.glb", "left_finger.glb", "right_finger.glb"):
        obsolete = (OUT / "panda" / name).resolve()
        assert obsolete.is_relative_to((OUT / "panda").resolve())
        obsolete.unlink(missing_ok=True)


def urdf_origin(element):
    if element is None:
        return np.eye(4)
    xyz = list(map(float, element.get("xyz", "0 0 0").split()))
    rpy = list(map(float, element.get("rpy", "0 0 0").split()))
    result = trimesh.transformations.euler_matrix(*rpy, axes="sxyz")
    result[:3, 3] = xyz
    return result


def kiwi(source):
    urdf = source / "urdf/kiwi_gripper.urdf"
    root = ET.parse(urdf).getroot()
    joints = {joint.find("child").get("link"): joint for joint in root.findall("joint")}
    indices = {link.get("name"): i for i, link in enumerate(root.findall("link"))}
    links = []
    motion = {}
    for spec in root.findall("link"):
        name = spec.get("name")
        joint = joints.get(name)
        frame = urdf_origin(joint.find("origin") if joint is not None else None)
        link = {"name": name, "parent": indices[joint.find("parent").get("link")] if joint is not None else -1,
                "pos": frame[:3, 3].tolist(), "quat": trimesh.transformations.quaternion_from_matrix(frame).tolist(),
                "joint": None}
        if joint is not None and joint.get("type") == "revolute":
            limit = joint.find("limit")
            limits = [float(limit.get("lower")), float(limit.get("upper"))]
            link["joint"] = {"name": joint.get("name"), "type": "hinge",
                             "axis": list(map(float, joint.find("axis").get("xyz").split())), "range": limits}
            # Both jaws use the same opening angle on opposite hinge axes.
            motion[joint.get("name")] = limits
        scene = trimesh.Scene()
        for visual in spec.findall("visual"):
            mesh_spec = visual.find("geometry/mesh")
            material = visual.find("material")
            # The detailed servo loses small protrusions at the default budget.
            budget = 12000 if material.get("name") == "servo" else FACE_BUDGET
            mesh = trimesh.load(urdf.parent / mesh_spec.get("filename"), force="mesh")
            if material.get("name") == "fasteners":
                # Simplify each fastener separately so entire small bolts cannot disappear.
                parts = mesh.split(only_watertight=False)
                mesh = trimesh.util.concatenate([
                    compact(part, max(100, round(budget * len(part.faces) / len(mesh.faces)))) for part in parts])
            else:
                mesh = compact(mesh, budget)
            scale = np.diag([*map(float, mesh_spec.get("scale", "1 1 1").split()), 1])
            mesh.apply_transform(urdf_origin(visual.find("origin")) @ scale)
            rgba = list(map(float, material.find("color").get("rgba").split()))
            scene.add_geometry(colored(mesh, rgba), node_name=material.get("name"))
        if scene.geometry:
            save_scene(scene, OUT / "kiwi-kuka" / f"{name}.glb")
            link["mesh"] = f"../kiwi-kuka/{name}.glb"
        links.append(link)
    attach("iiwa", links, [0, 0, 0.045], {"open": 0.04, "joints": motion})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kiwi_source", type=Path, help="Directory containing urdf/kiwi_gripper.urdf")
    args = parser.parse_args()
    robotiq()
    kiwi(args.kiwi_source)
