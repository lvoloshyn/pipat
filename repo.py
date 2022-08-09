# https://peps.python.org/pep-0503/

# Actual PYPI index at: https://pypi.org/simple/pandas/
# Additional package data at https://pypi.org/pypi/{package_name}/json
import datetime
import os
from dataclasses import dataclass

import requests
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")
PORT = os.environ.get("PORT", 8000)


@dataclass
class PythonPackageVersion:
    filename: str
    url: str
    version: str
    hash_string: str
    requires_python: str
    upload_time: datetime.datetime


class PythonPackage:
    def __init__(self, package_name: str):
        self._package_name = package_name

    def get_package_info(self):
        url = f"https://pypi.python.org/pypi/{self._package_name}/json"
        response = requests.get(url).json()
        return response

    def get_package_versions(self):
        info = self.get_package_info()

        result = []
        for version, files in info["releases"].items():
            for file_data in files:
                filename = file_data["filename"]
                dt = datetime.datetime.fromisoformat(file_data["upload_time"])

                hash_string = "md5=%s" % file_data["md5_digest"]
                if "sha256" in file_data["digests"]:
                    hash_string = "sha256=%s" % file_data["digests"]["sha256"]

                result.append(PythonPackageVersion(
                    filename=filename,
                    url=file_data["url"],
                    version=version,
                    hash_string=hash_string,
                    requires_python=file_data["requires_python"],
                    upload_time=dt
                ))

        return result

    def get_package_versions_at(self, year: int, month: int, day: int):
        dt_now = datetime.datetime(year=year, month=month, day=day, hour=0, minute=0, second=0)
        versions_data = self.get_package_versions()

        actual_versions = [item for item in versions_data if item.upload_time <= dt_now]
        actual_versions = sorted(actual_versions, key=lambda x: x.upload_time, reverse=True)

        return actual_versions


@app.route("/<int:year>-<int:month>-<int:day>/<string:package>")
def get_package_versions_at(year: int, month: int, day: int, package: str):
    p = PythonPackage(package)
    releases = p.get_package_versions_at(year=year, month=month, day=day)
    return render_template("package.html", package=package, releases=releases)


if __name__ == "__main__":
    print("Example (for Feb 24, 2016):")
    print(f"$ pip install -i http://localhost:{PORT}/2016-02-24/ -r requirements.txt\n\n\n")
    app.run(host="127.0.0.1", port=PORT, debug=False)
