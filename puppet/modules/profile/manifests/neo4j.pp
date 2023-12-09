class profile::neo4j {
  package { ['java-1.8.0-openjdk-devel', 'python3-pip']:
    ensure => installed,
  }

  class { 'neo4j':
    version => '3.5.14',
    require => Package['java-1.8.0-openjdk-devel'],
  }

  package { 'neo4j':
    ensure   => installed,
    provider => 'pip3',
    require  => Package['python3-pip'],
  }
}