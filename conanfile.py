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
    options = {"shared": [True, False],
               "fPIC": [True, False], }
    default_options = {"shared": True,
                       "fPIC": True, }
    generators = "cmake"
    _cmake = None

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(source_folder="libuvc")
        return self._cmake

    def source(self):
        self.run("git clone https://github.com/libuvc/libuvc.git")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        cmake.patch_config_paths()
        self.copy("LICENSE.txt", src="libuvc", dst="licenses")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "libuvc"
        self.cpp_info.names["cmake_find_package_multi"] = "libuvc"
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include/libuvc/"]
