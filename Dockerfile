FROM anibali/pytorch:cuda-10.1

COPY . /app

# Install Conda dependencies
RUN conda env create -f /app/environment.yml && \
    conda clean -fay
