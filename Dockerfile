FROM anibali/pytorch:cuda-10.1

COPY . /app

# Install Conda dependencies

RUN conda env create -f /app/environment.yaml && \
    conda clean -fay

ENV BASH_ENV ~/.bashrc

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate cv" >> ~/.bashrc

SHELL ["/bin/bash","-c"]

COPY packages ./packages

RUN pip install pdf2image Augmentor --no-index --find-links file:///packages/


CMD ["/bin/bash"]