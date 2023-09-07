exec { 'update_system':
  command => '/usr/bin/env apt-get update -y',
}

package { 'nginx':
  ensure => 'installed',
}

file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

$index_html_content = '
<html>
<head>
</head>
<body>
  <p>Nginx server test</p>
</body>
</html>
'

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => $index_html_content,
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

exec { 'chown_data':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin:/usr/local/bin:/bin',
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => template('your_module/nginx_config.erb'), # You need to create a template for the nginx configuration
}

service { 'nginx':
  ensure => 'running',
}
