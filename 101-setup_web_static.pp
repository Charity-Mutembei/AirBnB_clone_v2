# Install Nginx and update the system
class { 'nginx': }

# Create necessary directories
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

# Create the HTML content and write it to index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>',
}

# Create symbolic link to current
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership to ubuntu:ubuntu
exec { 'set_owner':
  command => 'chown -R ubuntu:ubuntu /data',
  path    => ['/bin', '/usr/bin'],
  require => File['/data/web_static/current'],
}

# Configure Nginx to serve the content
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "server {
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}",
  require => Class['nginx'],
}

# Restart Nginx for configuration changes
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
