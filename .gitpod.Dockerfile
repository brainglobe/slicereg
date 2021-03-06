FROM gitpod/workspace-full-vnc

RUN apt-get install -y x11-utils libxkbcommon-x11-0
# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
