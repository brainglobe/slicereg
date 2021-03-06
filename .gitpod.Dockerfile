FROM gitpod/workspace-full-vnc

# Have all the qt stuff appear upon running (easier to debug root problems)
ENV QT_DEBUG_PLUGINS=1

# Have poetry use global pip by default (pip install --user isn't working in docker for some reason)
ENV PIP_USER=false 

# Install linux packages
RUN sudo apt-get update \ 
    && sudo apt-get install -y \
    mesa-utils freeglut3-dev \
    libgl1 \ 
    libxkbcommon-x11-0 \ 
    x11-xserver-utils \
    && sudo rm -rf /var/lib/apt/lists/*


# Maybe need:
# libx11-xcb1 \
# libxkbcommon-x11-0 \  # needed for qt's xcb 
# x11-xserver-utils   # gets xrandr, used for setting/determining screen resolution
# x11-apps  # provides xeyes, a nice test for if graphics are working at all on x11
# libgtk-3-dev 
# mesa-utils freeglut3-dev   # gl funcs and glu funcs
# libsdl2-dev

# Install python package manager
RUN python -m pip install --upgrade pip \
    && pip install poetry 

# Install python packages    
RUN poetry install

