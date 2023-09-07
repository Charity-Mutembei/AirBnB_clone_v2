# Update the package list and install Nginx
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory',
}

# Create an HTML file for the test page
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

# Create a symbolic link to the test release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership to ubuntu:ubuntu
file { '/data':
  owner => 'ubuntu',
  group => 'ubuntu',
  recurse => true,
}

# Configure Nginx to serve the content
file { '/etc/nginx/sites-available/web_static':
  ensure  => 'file',
  content => "server {
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}",
}

# Create a symbolic link to enable the site
file { '/etc/nginx/sites-enabled/web_static':
  ensure => 'link',
  target => '/etc/nginx/sites-available/web_static',
}

# Restart Nginx for configuration changes
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/web_static'],
}