# Twintelligence

Twintelligence is a free Twitter OSINT tool

## Author 

Jean-Philippe Teissier - @Jipe_ 

## Development status

**FECT is no longer maintained**

## How to install

Copy all files from Github

## Dependencies

* pip install python-twitter
* pip install flask

If you want to run it with Nginx and uwsgi

* apt-get install nginx uwsgi uwsgi-plugin-python

## Setup

1. Create an application. See https://dev.twitter.com/ 

2. Go to your application's settings -> OAuth settings and copy/paste your "Consumer key" and your "Consumer key" to the YOUR_APP_CONSUMER_KEY and YOUR_APP_CONSUMER_SECRET variables in the source code

3. Go to your application's settings -> Application Type, and change the Access parameter to "Read, Write and Access direct messages". Update the settings

3. Go back to your application's details and click on "Recreate my access token". Copy/paste your "Access token" and your "Access token secret" to the YOUR_ACCESS_TOKEN_SECRET and YOUR_ACCESS_TOKEN in the source code. Alternatively you can pass them as arguments with -k/--accesstokenkey and -s/accesstokensecret

## How to run

python twintelligence.py

## Changelog

### 0.2
 * python-twitter & API model update

### 0.1
 * Initial alpha release

## License

Twintelligence
Copyright (C) 2013-2016 Jean-Philippe Teissier

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
