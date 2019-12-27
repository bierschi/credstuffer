# credstuffer
[![Build Status](https://travis-ci.org/bierschi/credstuffer.png?branch=master)](https://travis-ci.org/bierschi/credstuffer) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


## Installation

install [credstuffer](https://github.com/bierschi/credstuffer) with pip
<pre><code>
pip3 install credstuffer
</code></pre>

or from source
<pre><code>
sudo python3 setup.py install
</code></pre>


## Usage and Examples

Print the available arguments for credstuffer
<pre><code>
credstuffer --help
</code></pre>

Use it with a credential file of your choice
<pre><code>
credstuffer instagram file --path /home/john/credentials.txt
</code></pre>

Fetch data from a database connection
<pre><code>
credstuffer instagram database --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname postgres
</code></pre>

## Logs

logs can be found in `/var/log/credstuffer`

## Troubleshooting
add your current user to group `syslog`, this allows the application/scripts to create a folder in
`/var/log`. Replace `<user>` with your current user
<pre><code>
sudo adduser &lt;user&gt; syslog
</code></pre>
to apply this change, log out and log in again and check with the terminal command `groups`

## Changelog
All changes and versioning information can be found in the [CHANGELOG](https://github.com/bierschi/credstuffer/blob/master/CHANGELOG.rst)

## License
Copyright (c) 2019 Bierschneider Christian. See [LICENSE](https://github.com/bierschi/credstuffer/blob/master/LICENSE)
for details


