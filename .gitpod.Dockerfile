FROM gitpod/workspace-full-vnc

RUN sudo apt-get update && sudo apt-get install -y x11-apps
# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
