project(
  'pyoorb',
  'fortran',
  version: run_command(['python', 'build-tools/gitversion.py'], check: true).stdout().strip(),
  meson_version: '>=1.2.0'
)

py = import('python').find_installation(pure: false)

min_numpy_version = '2.0.0'  # keep in sync with pyproject.toml
min_python_version = '3.10'   # keep in sync with pyproject.toml

python_version = py.language_version()
if python_version.version_compare(f'<@min_python_version@')
  error(f'Minimum supported Python version is @min_python_version@, found @python_version@')
endif

fc = meson.get_compiler('fortran')

# match meson compiler IDs with ./configure's expected strings
if fc.get_id() == 'gcc'
  configure_fc = 'gfortran'
else
  configure_fc = fc
endif

f2py_bin = run_command(['which', 'f2py'], check: true).stdout().splitlines()[0]

run_command(
  './configure',
  configure_fc,
  'opt',
  '--with-pyoorb',
  '--with-f2py',
  f2py_bin,
  '--with-python',
  py.full_path(),
  check: true
)

run_command('make', '-j4', check: true)

inc = include_directories('build')

py.extension_module(
  'pyoorb',
  'python/pyoorb.f90',
  install: true,
  include_directories: inc
)
