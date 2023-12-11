class profile::flask_api {
  package { 'python3':
    ensure => installed,
  }

  package { 'uwsgi':
    ensure => installed,
  }

 file { '/project_oneplanet_zorgtechnologie_app/api/src/main/python':
    ensure => directory,
  }

  file { '/etc/uwsgi/apps-available/flask-api.ini':
    content => '
[uwsgi]
chdir = chdir = /project_oneplanet_zorgtechnologie_app
module = api.src.main.python.database_api:app
master = true
processes = 4
socket = 0.0.0.0:5001
vacuum = true
    ',
  }

  file { '/etc/systemd/system/uwsgi.service':
    content => '
[Unit]
Description=uWSGI

[Service]
ExecStart=/usr/bin/uwsgi --ini /etc/uwsgi/apps-available/flask-api.ini
Restart=always

[Install]
WantedBy=default.target
    ',
  }

  service { 'uwsgi':
    ensure => running,
    enable => true,
  }
}