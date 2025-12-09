project(
  'pyoorb',
  'fortran',
#   version: run_command(['cat', 'VERSION'], check: true).stdout().strip(),
  version: run_command(['python', '-m', 'setuptools_scm']).stdout().strip(),
  meson_version: '>=1.2.0'
)

py = import('python').find_installation(pure: false)
fc = meson.get_compiler('fortran')
f2py_bin = run_command(['which', 'f2py'], check: true).stdout().splitlines()[0]

# match meson compiler IDs with ./configure's expected strings
if fc.get_id() == 'gcc'
  configure_fc = 'gfortran'
else
  configure_fc = fc
endif

run_command(
  './configure',
  configure_fc,
  'opt',
#   '--with-pyoorb',
#   '--with-f2py',
#   f2py_bin,
#   '--with-python',
#   py.full_path(),
  check: true
)

liboorb = custom_target(
  'liboorb',
  output: 'liboorb.a',
  command : ['make', '-C' , '..', '-j4']
#   command : ['ls']
)

# liboorb_dep = declare_dependency(
#     link_with: liboorb,
#     include_directories: include_directories('build')
# )

py.extension_module(
  'pyoorb',
  ['python/pyoorb.f90', liboorb],
  include_directories: include_directories('build'),
  install: true,
)
