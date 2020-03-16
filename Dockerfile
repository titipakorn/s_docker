FROM anibali/pytorch:cuda-10.1

COPY . /app

# Install Conda dependencies

RUN conda env create -f /app/environment.yaml && \
    conda clean -fay

RUN conda activate cv

COPY packages ./packages

RUN pip3 install pdf2image Augmentor --no-index --find-links file:///packages/


CMD ["/bin/bash"]