FROM gitpod/workspace-full

ENV DISPLAY :99.0

RUN sudo apt-get update && sudo apt-get install -y xvfb x11-utils libxkbcommon-x11-0
RUN python -m pip install --upgrade
RUN python -m pip install poetry