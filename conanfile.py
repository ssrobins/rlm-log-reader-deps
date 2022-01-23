from conans import ConanFile

class Conan(ConanFile):
    name = "RLMLogReaderDeps"
    version = "0.0.1"
    settings = "os"
    generators = "cmake"

    def requirements(self):
        self.requires("boost/1.78.0")
        self.requires("date/3.0.1")
        self.requires("gtest/1.11.0")
        self.requires("qt/5.15.2")
        self.requires("expat/2.4.2")
        self.requires("openssl/1.1.1l")
