class profile::flask_api {
  package { 'python3':
    ensure => installed,
  }

  package { 'gunicorn':
    ensure => installed,
  }

  file { 'api/src/main/python/database_api.py':
    ensure => directory,
  }

  file { '/etc/systemd/system/flask-api.service':
    content => '
[Unit]
Description=Flask API

[Service]
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:5001 your_flask_app:app
WorkingDirectory=api/src/main/python/database_api.py
Restart=always

[Install]
WantedBy=default.target
    ',
  }

  service { 'flask-api':
    ensure => running,
    enable => true,
  }
}