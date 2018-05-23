from conans import ConanFile, MSBuild


class Hello(ConanFile):
    name = "Hello"
    version = "01.01.01"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "Hello2015/*", "*.vcxproj*", "*.sln*"

    def build(self):
    ¦   msbuild = MSBuild(self)
    ¦   msbuild.build("Hello2015.sln")

    def package(self):
    ¦   self.copy("*.h", dst="include", src="Hello2015")
    ¦   self.copy("*.dll", dst="dll", keep_path=False)

    def package_info(self):
    ¦   self.cpp_info.libs = ["Hello2015"]
