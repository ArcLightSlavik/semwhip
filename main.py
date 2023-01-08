from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pydantic import BaseModel

from fastapi import FastAPI

import httpx

app = FastAPI()


class PackageVersions(BaseModel):
    package_name: str
    versions: dict[str, bool]


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/{package_name}")
def get_package_versions(package_name: str):
    response = httpx.get(f"https://pypi.org/pypi/{package_name}/json")
    releases_data = response.json()["releases"].keys()
    sorted_releases = sorted(releases_data, key=Version)
    final_versions = {ver: False for ver in sorted_releases}
    return PackageVersions(package_name=package_name, versions=final_versions)


@app.get("/constraint/{package_name}")
def get_package_versions_constraint(package_name: str, constraint: str) -> PackageVersions:
    constraint = SpecifierSet(constraint)
    response = httpx.get(f"https://pypi.org/pypi/{package_name}/json")
    releases_data = response.json()["releases"].keys()
    sorted_releases = sorted(releases_data, key=Version)
    constrained_list = {ver: (True if ver in constraint else False) for ver in sorted_releases}
    return PackageVersions(package_name=package_name, versions=constrained_list)
