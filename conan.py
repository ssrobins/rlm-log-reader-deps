#!/usr/bin/env python3

import argparse
import os.path
import subprocess

def main():
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"
    os.environ["CONAN_SYSREQUIRES_MODED"] = "enabled"

    platform = {
        "linux": "-s compiler=gcc -s compiler.version=7 -s compiler.libcxx=libstdc++11 -s compiler.cppstd=17",
        "macos": "-s os.version=10.13 -s compiler.version=13.1 -s compiler.cppstd=17",
        "windows": "-s arch=x86 -s compiler=\"Visual Studio\" -s compiler.version=17 -s compiler.runtime=MT -s compiler.cppstd=17"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    parser.add_argument("--config", help="Build config")
    command_args = parser.parse_args()

    script_path = os.path.dirname(os.path.realpath(__file__))

    if command_args.config:
        config = f"-s build_type={command_args.config}"
    else:
        config = "-s build_type=Debug"

    conan_options = " ".join([
    "-o qt:qt3d=False",
    "-o qt:qtactiveqt=False",
    "-o qt:qtandroidextras=False",
    "-o qt:qtcharts=False",
    "-o qt:qtconnectivity=False",
    "-o qt:qtdatavis3d=False",
    "-o qt:qtdeclarative=False",
    "-o qt:qtdoc=False",
    "-o qt:qtgamepad=False",
    "-o qt:qtgraphicaleffects=False",
    "-o qt:qtimageformats=False",
    "-o qt:qtlocation=False",
    "-o qt:qtlottie=False",
    "-o qt:qtmacextras=False",
    "-o qt:qtmultimedia=False",
    "-o qt:qtnetworkauth=False",
    "-o qt:qtpurchasing=False",
    "-o qt:qtquick3d=False",
    "-o qt:qtquickcontrols=False",
    "-o qt:qtquickcontrols2=False",
    "-o qt:qtquicktimeline=False",
    "-o qt:qtremoteobjects=False",
    "-o qt:qtscript=False",
    "-o qt:qtscxml=False",
    "-o qt:qtsensors=False",
    "-o qt:qtserialbus=False",
    "-o qt:qtserialport=False",
    "-o qt:qtspeech=False",
    "-o qt:qtsvg=False",
    "-o qt:qttools=False",
    "-o qt:qttranslations=False",
    "-o qt:qtvirtualkeyboard=False",
    "-o qt:qtwayland=False",
    "-o qt:qtwebchannel=False",
    "-o qt:qtwebengine=False",
    "-o qt:qtwebglplugin=False",
    "-o qt:qtwebsockets=False",
    "-o qt:qtwebview=False",
    "-o qt:qtwinextras=False",
    "-o qt:qtx11extras=False",
    "-o qt:qtxmlpatterns=False"
    ])

    remote_url = "https://center.conan.io"
    conan_remote = f"conan remote add conancenter {remote_url} --insert --force"
    print(conan_remote, flush=True)
    subprocess.run(conan_remote, cwd=script_path, shell=True, check=True)

    conan_create = f"conan create --update . {platform[command_args.platform]} {conan_options} {config} --build=missing"
    print(conan_create, flush=True)
    subprocess.run(conan_create, cwd=script_path, shell=True, check=True, env=os.environ.copy())


if __name__ == "__main__":
    main()
