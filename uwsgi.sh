#!/bin/bash
### BEGIN INIT INFO
# Provides:          uwsgi
# Required-Start:    $local_fs $remote_fs $network
# Required-Stop:     $local_fs $remote_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start/stop uWSGI server instance(s)
# Description:       This script manages uWSGI server instance(s).
#                    You could control specific instance(s) by issuing:
#                    
#                        service uwsgi <command> <confname> <confname> ...
#                    
#                    You can issue to init.d script following commands:
#                      * start        | starts daemon
#                      * stop         | stops daemon
#                      * reload       | sends to daemon SIGHUP signal
#                      * force-reload | sends to daemon SIGTERM signal
#                      * restart      | issues 'stop', then 'start' commands
#                      * status       | shows status of daemon instance
#                    
#                    'status' command must be issued with exactly one
#                    argument: '<confname>'.
#                    
#                    In init.d script output:
#                      * . -- command was executed without problems or instance
#                             is already in needed state
#                      * ! -- command failed (or executed with some problems)
#                      * ? -- configuration file for this instance isn't found
#                             and this instance is ignored
#                    
#                    For more details see /usr/share/doc/uwsgi/README.Debian.
### END INIT INFO

/usr/bin/uwsgi -y /usr/share/nginx/www/uwsgi.yaml --uid www-data --gid www-data