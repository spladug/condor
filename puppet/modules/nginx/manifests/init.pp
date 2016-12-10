class nginx {
  package { 'nginx':
    ensure => installed,
  }

  file { '/etc/nginx/sites-enabled/default':
    ensure  => absent,
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/condor':
    ensure  => file,
    source  => 'puppet:///modules/nginx/condor.nginx',
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    notify  => Service['nginx'],
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-enabled/condor':
    ensure  => link,
    target  => '/etc/nginx/sites-available/condor',
    require => Package['nginx'],
  }

  service { 'nginx':
    ensure  => running,
    require => [
      File['/etc/nginx/sites-enabled/condor'],
      Package['nginx'],
    ],
  }
}
