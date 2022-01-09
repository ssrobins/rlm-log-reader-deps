#!/usr/bin/env python3

import json
import os.path
import subprocess

def main():
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    # platform = {
    #     "androidarm": "-s os=Android -s os.api_level=16 -s arch=armv7 -s compiler=clang -s compiler.version=12 -s compiler.libcxx=c++_static -s compiler.cppstd=17",
    #     "androidarm64": "-s os=Android -s os.api_level=21 -s arch=armv8 -s compiler=clang -s compiler.version=12 -s compiler.libcxx=c++_static -s compiler.cppstd=17",
    #     "ios": "-s os=iOS -s arch=armv7 -s os.version=9.0 -s compiler.version=13.0 -s compiler.cppstd=17",
    #     "linux": "-s compiler=gcc -s compiler.version=7 -s compiler.libcxx=libstdc++11 -s compiler.cppstd=17",
    #     "macos": "-s os.version=10.9 -s compiler.version=13.0 -s compiler.cppstd=17",
    #     "windows": "-s arch=x86 -s compiler=msvc -s compiler.version=193 -s compiler.runtime=static -s compiler.cppstd=17"
    # }

    # parser = argparse.ArgumentParser()
    # parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    # command_args = parser.parse_args()

    script_path = os.path.dirname(os.path.realpath(__file__))

    remote_url = "https://ssrobins.jfrog.io/artifactory/api/conan/conan"
    conan_remote = f"conan remote add artifactory-ssrobins {remote_url} --insert --force"
    print(conan_remote, flush=True)
    subprocess.run(conan_remote, cwd=script_path, shell=True, check=True)

    conan_info = f"conan info . --json"
    conan_info_output = subprocess.run(conan_info, cwd=script_path, shell=True, check=True, stdout=subprocess.PIPE)

    conan_info_json = json.loads(conan_info_output.stdout)

    for item in conan_info_json:
        package_reference = item["reference"]
        if "conanfile.py" not in package_reference:
            conan_upload = f"conan upload {package_reference} --all --remote artifactory-ssrobins --confirm --parallel"
            subprocess.run(conan_upload, cwd=script_path, shell=True, check=True)

if __name__ == "__main__":
    main()
