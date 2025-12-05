import os
import subprocess
import shutil
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path


extension = Extension(
    name="pyoorb", sources=["pyoorb.f90", "pyoorb.pyf"], include_dirs=["../build"]
)


class PyoorbBuild(build_ext):
    def run(self):
        self.configure()
        for ext in self.extensions:
            self.build_extension(ext)

    def configure(self):
        fortran_compiler = os.environ.get("FC", "gfortran")
        f2py_bin = shutil.which("f2py")
        py_bin = shutil.which("python")
        if py_bin is None:
            py_bin = shutil.which("python3")
        self.spawn(
            [
                "./configure",
                fortran_compiler,
                "opt",
                "--with-pyoorb",
                "--with-f2py",
                f2py_bin,
                "--with-python",
                py_bin,
            ]
        )

    def build_extension(self, ext):
        try:
            self.spawn(["make", "-j4"])
            self.spawn(["make", "pyoorb", "-j4"])
        finally:
            os.chdir("./python")

        src = "../lib/" + self.get_ext_filename(ext.name)
        dst = self.get_ext_fullpath(ext.name)
        self.mkpath(os.path.dirname(dst))
        self.copy_file(src, dst)


def deduce_version():
    # This is a gnarly hack, but it ensures consistency.
    stdout = subprocess.PIPE
    cmd_output = subprocess.run(
        ["./build-tools/compute-version.sh", "-u"],
        stdout=stdout,
    )
    cmd_output.check_returncode()
    return cmd_output.stdout.decode("utf8").strip()


# setup(
#     ext_modules=[extension],
#     install_requires=["numpy"],
#     cmdclass={
#         "build_ext": PyoorbBuild,
#     }
# )
