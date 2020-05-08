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
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

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

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = [
            f"{self._build_subfolder}/include/libuvc/"]
