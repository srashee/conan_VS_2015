from conans import ConanFile, MSBuild, AutoToolsBuildEnvironment, tools
##################################################################
#                CROSS-COMPILATION CONANFILE                     #
##################################################################
#                                                                #
# Windows Build System: Visual Studio -- MSBuild                 #
#                                                                #
# Linux Build System: GNU Make / AutoToolsBuildEnvironment       #
##################################################################
# Fill in Requires with the Conan Package needed to compile this #
# Project. The imports method will copy over all libraries or    #
# even executables needed to run this project in a folder called #
# bin created in the same directory as this conanfile            #
##################################################################
#NOTE: Please read and configure this template before using this #
# is not plug and play.                                          #
##################################################################
class Hello(ConanFile):
    name = "Hello"
    version = "01.01.01"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "ConanHelloVS/*", "*.vcxproj*", "*.sln*"
    generators = "visual_studio"
    #requires = "Example/00.00.00@linux/release"

    def imports(self):
        self.copy("*.so", src="bin", dst="bin")
        self.copy("*.dll", src="bin", dst="bin")
        self.copy("*.exe", src="bin", dst="bin")
        self.copy("Hello", src="bin", dst="bin")

    # The windows solution is built using MSBuild and for the
    # platform Win32. The Win32 target has been deprecated but
    # to build for that target you must include the platforms
    # argument below.
    #
    # The Linux build is built using a makefile with the
    # Autotools helper. It exports the include path to what
    # was specified in 'requires'
    def build(self):
        if self.settings.os == "Windows":
            msbuild = MSBuild(self)
            msbuild.build("ConanHelloVS.sln", platforms={"x86": "Win32"})
        else:
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_appen(env_build.vars):
                self.run("Make -C ConanHelloVS -f Makefile.mk")

    # NOTE: This must be configured to ensure imported
    # binaries from other packages aren't package in here.
    # If the package is ready to be commited or released we
    # we copy all the headers and bibaries into the local cache
    # ready for deployment
    def package(self):
        self.copy("*.h", dst="include", src="ConanHelloVS")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.a", dst="bin", keep_path=False)
        self.copy("*.lib", dst="bin", keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("Hello", dst="bin", keep_path=FalsE)

    # This method is used for specifying information for the
    # consumers of this package
    def package_info(self):
        self.cpp_info.libs = ["ConanHelloVS"]
