from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

import os


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
               "fPIC": [True, False],
               "example": [True, False],
               "test": [True, False],
               }
    default_options = {"shared": False,
                       "fPIC": True,
                       "example": True,
                       "test": False,
                       }
    generators = "cmake"
    exports_sources = ["CMakeLists.txt"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.compiler == "Visual Studio":
            # Upstream issues, e.g.:
            # https://github.com/libuvc/libuvc/issues/100
            # https://github.com/libuvc/libuvc/issues/105
            raise ConanInvalidConfiguration(
                "Library is incompatible with Windows")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        cmake = self._cmake
        cmake.definitions["BUILD_EXAMPLE"] = self.options.example
        cmake.definitions["BUILD_TEST"] = self.options.test
        cmake.configure(source_folder=self._source_subfolder,
                        build_folder=self._build_subfolder)
        return cmake

    def requirements(self):
        self.requires("libusb/1.0.23")
        if self.options.test:
            self.requires("opencv/4.1.1@conan/stable")

    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone("https://github.com/libuvc/libuvc.git", "master")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        cmake.patch_config_paths()
        self.copy("LICENSE.txt", src=self._source_subfolder, dst="licenses")
        self.copy("*.h", dst="include",
                  src=os.path.join(self._source_subfolder, "include"))
        self.copy("*.h", dst="include",
                  src=os.path.join(self._build_subfolder, "include"))
        if not self.options.shared:
            self.copy("libuvc.a", dst="lib",
                      src=self._build_subfolder, keep_path=False)
            return
        """
        if self.settings.os == "Macos":
            self.copy("libuvc.dylib", dst="lib",
                      src=self._build_subfolder, keep_path=False)
        else:
            self.copy("libuvc.so", dst="lib",
                      src=self._build_subfolder, keep_path=False)
        """

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
