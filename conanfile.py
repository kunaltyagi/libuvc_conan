from conans import ConanFile, CMake, tools


class LibuvcConan(ConanFile):
    name = "libuvc"
    version = "0.1"
    license = "BSD"
    author = "Kunal Tyagi <tyagi.kunal@live.com>"
    url = "https://github.com/libuvc/libuvc"
    description = "a cross-platform library for USB video devices"
    topics = ("c", "camera", "usb")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/libuvc/libuvc.git")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="libuvc")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="libuvc/src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libuvc"]

