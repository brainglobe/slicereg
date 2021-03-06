FROM gitpod/workspace-full-vnc

RUN sudo apt-get update \ 
    && sudo apt-get install -y mesa-utils x11-utils \
    && sudo rm -rf /var/lib/apt/lists/*

ENV QT_DEBUG_PLUGINS=1
# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/


# Maybe need:
#  libxkbcommon-x11-0 \