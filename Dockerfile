FROM anibali/pytorch:cuda-10.1

COPY . /app

# Install Conda dependencies
RUN conda update --prefix /home/user/miniconda/envs/py36 anaconda

RUN conda env create -f /app/environment.yaml && \
    conda clean -fay

CMD ["/bin/bash"]