# 1. --- Install System Dependencies ---
# wkhtmltopdf is not in the default Debian (slim) repos.
# We must download and install it manually.
# We also need wget (to download) and other font dependencies.
RUN apt-get update \
    && apt-get install -y \
    wget \
    fontconfig \
    libxrender1 \
    libxext6 \
    xfonts-75dpi \
    xfonts-base \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    # Install any missing dependencies that dpkg might have noted
    && apt-get install -y -f \
    # Clean up
    && rm wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
