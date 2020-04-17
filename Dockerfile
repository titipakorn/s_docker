FROM anibali/pytorch:cuda-10.1

COPY . /app

# Install Conda dependencies

RUN conda env create -f /app/environment.yaml && \
    conda clean -fay

ENV BASH_ENV ~/.bashrc

SHELL ["conda","run","-n","cv","/bin/bash","-c"]

COPY packages ./packages

RUN pip install pdf2image Augmentor --no-index --find-links="./packages"

CMD ["/bin/bash"]