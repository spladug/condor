class condor {
  $dependencies = [
    'python',
    'python-dev',
    'python-gevent',
    'python-setuptools',
  ]

  package { $dependencies:
    ensure => installed,
    before => Exec['install app'],
  }

  exec { 'install app':
    user      => $::user,
    cwd       => $::project_path,
    command   => 'python setup.py develop --user',
    logoutput => true,
  }
}
