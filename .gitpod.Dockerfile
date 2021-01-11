FROM gitpod/workspace-full

ENV DISPLAY :99.0

RUN sudo apt install -y xvfb x11-utils libxkbcommon-x11-0
