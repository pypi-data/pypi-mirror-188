import io
import json
import os
import pickle
import sys
import zipfile

import torch

from autumn8.lib.package_resolver import package
from autumn8.common._version import __version__

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))


def write_model(model, dummy_input, bytes):
    traced = torch.jit.trace(model, dummy_input)
    traced.save(bytes)


def export_tensorflow_model_repr(
    model,
    dummy_input,
    interns=[],
    externs=[],
    max_search_depth=5,
    preprocess=None,
    postprocess=None,
):
    return export_model_repr(
        model,
        dummy_input,
        "TENSORFLOW",
        interns,
        externs,
        max_search_depth,
        preprocess,
        postprocess,
    )


def export_pytorch_model_repr(
    model,
    dummy_input,
    interns=[],
    externs=[],
    max_search_depth=5,
    preprocess=None,
    postprocess=None,
):
    return export_model_repr(
        model,
        dummy_input,
        "PYTORCH",
        interns,
        externs,
        max_search_depth,
        preprocess,
        postprocess,
    )


def export_model_repr(
    model,
    dummy_input,
    framework,
    interns=[],
    externs=[],
    max_search_depth=5,
    preprocess=None,
    postprocess=None,
):
    bytes = io.BytesIO()

    if not isinstance(dummy_input, tuple):
        dummy_input = (dummy_input,)

    if framework == "PYTORCH":
        externs.append("torch")
        externs.append("torchvision")

    if framework == "TENSORFLOW":
        externs.append("tensorflow")

    file, requirements, package_name = package(
        model, interns, externs, max_search_depth
    )

    (
        file_preprocess,
        requirements_preprocess,
        package_name_preprocess,
        file_postprocess,
        requirements_postprocess,
        package_name_postprocess,
    ) = [None for i in range(6)]

    if preprocess is not None:
        (
            file_preprocess,
            requirements_preprocess,
            package_name_preprocess,
        ) = package(preprocess, interns, externs, max_search_depth)
        requirements.update(requirements_preprocess)

    if postprocess is not None:
        (
            file_postprocess,
            requirements_postprocess,
            package_name_postprocess,
        ) = package(postprocess, interns, externs, max_search_depth)
        requirements.update(requirements_postprocess)
    with zipfile.ZipFile(bytes, "w") as zip:
        zip.writestr(
            "MANIFEST",
            json.dumps(
                {
                    "version": __version__,
                    "package_name": package_name,
                    "package_name_preprocess": package_name_preprocess,
                    "package_name_postprocess": package_name_postprocess,
                }
            ),
        )
        zip.write(file.name, arcname="model.package")
        if file_preprocess is not None:
            zip.write(file_preprocess.name, arcname="preprocess.package")
        if file_postprocess is not None:
            zip.write(file_postprocess.name, arcname="postprocess.package")
        requirement_list = []
        for package_name, package_version in requirements.items():
            requirement_list.append(f"{package_name}=={package_version}")

        zip.writestr("requirements.txt", "\n".join(requirement_list))

    bytes.seek(0)
    return bytes


def load_model(filename):
    with zipfile.ZipFile(filename) as z:
        with z.open("MANIFEST", "r") as manifest:
            manifest_content = json.loads(manifest.read())
            package_name = manifest_content["package_name"]
            package_name_preprocess = manifest_content[
                "package_name_preprocess"
            ]
            package_name_postprocess = manifest_content[
                "package_name_postprocess"
            ]
        with z.open("model.package", "r") as model_file:
            resource_name = "model.pkl"
            imp = torch.package.PackageImporter(model_file)
            loaded_model = imp.load_pickle(package_name, resource_name)

        loaded_preprocess = None
        if package_name_preprocess is not None:
            with z.open("preprocess.package", "r") as model_file:
                resource_name = "model.pkl"
                imp = torch.package.PackageImporter(model_file)
                loaded_preprocess = imp.load_pickle(
                    package_name_preprocess, resource_name
                )

        loaded_postprocess = None
        if package_name_postprocess is not None:
            with z.open("postprocess.package", "r") as model_file:
                resource_name = "model.pkl"
                imp = torch.package.PackageImporter(model_file)
                loaded_postprocess = imp.load_pickle(
                    package_name_postprocess, resource_name
                )

        return loaded_model, loaded_preprocess, loaded_postprocess


attached_models = []


# TODO: create 'annotate' module?
def attach_model(
    model,
    example_input,
    interns=None,
    externs=None,
    max_search_depth=5,
    preprocess=None,
    postprocess=None,
):
    if interns is None:
        interns = []
    if externs is None:
        externs = []
    attached_models.append(
        (
            model,
            example_input,
            interns,
            externs,
            max_search_depth,
            preprocess,
            postprocess,
        )
    )
