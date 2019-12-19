# credstuffer
[![Build Status](https://travis-ci.org/bierschi/credstuffer.png?branch=master)](https://travis-ci.org/bierschi/credstuffer) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


## Installation

installation from source
<pre><code>
sudo python3 setup.py install
</code></pre>

or create a wheel for installing the package with pip
<pre><code>
sudo python3 setup.py bdist_wheel
</code></pre>

install the package with pip
<pre><code>
pip3 install CredentialDatabase-1.0.0-py3-none-any.whl
</code></pre>

uninstall the package with pip 
<pre><code>
pip3 uninstall CredentialDatabase
</code></pre>

### Usage and Examples



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


