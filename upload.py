#!/usr/bin/env python3

import json
import os.path
import subprocess
import tempfile

def main():
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    script_path = os.path.dirname(os.path.realpath(__file__))

    remote_url = "https://ssrobins.jfrog.io/artifactory/api/conan/conan"
    conan_remote = f"conan remote add artifactory-ssrobins {remote_url} --insert --force"
    print(conan_remote, flush=True)
    subprocess.run(conan_remote, cwd=script_path, shell=True, check=True)

    with tempfile.TemporaryDirectory() as json_path:
        conan_info_outfile = f"{json_path}/deps.json"
        conan_info = f"conan info . --json {conan_info_outfile}"
        print(conan_info, flush=True)
        subprocess.run(conan_info, cwd=script_path, shell=True, check=True)

        with open(conan_info_outfile) as conan_info_output:
            conan_info_json = json.load(conan_info_output)

    for item in conan_info_json:
        package_reference = item["reference"]
        if "conanfile.py" not in package_reference:
            conan_upload = f"conan upload {package_reference} --all --remote artifactory-ssrobins --confirm --parallel"
            print(conan_upload, flush=True)
            subprocess.run(conan_upload, cwd=script_path, shell=True, check=True)

if __name__ == "__main__":
    main()
