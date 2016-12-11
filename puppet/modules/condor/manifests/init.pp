class condor {
  exec { 'add reddit ppa':
    command => 'add-apt-repository -y ppa:reddit/ppa',
    unless  => 'apt-cache policy | grep reddit/ppa',
    notify  => Exec['update apt cache'],
  }

  $dependencies = [
    'python',
    'python-baseplate',
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

  exec { 'initialize database':
    user      => $::user,
    cwd       => $::project_path,
    command   => 'baseplate-script2 example.ini condor.models:create_schema',
    logoutput => true,
    require   => Exec['install app'],
  }

  file { '/etc/init/condor.conf':
    ensure => file,
    source => 'puppet:///modules/condor/condor.upstart',
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }

  service { 'condor':
    ensure => running,
  }
}
