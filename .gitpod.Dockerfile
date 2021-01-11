FROM gitpod/workspace-full-vnc

USER gitpod

RUN sudo apt-get update
RUN python -m pip install --upgrade
RUN python -m pip install poetry