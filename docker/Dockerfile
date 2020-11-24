FROM openjdk:8

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   curl \
                   ca-certificates \
                   python3 \
                   python3-pip && \
    rm -rf /var/lib/apt/lists

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    jupyter \
    pytest

WORKDIR /workspace
COPY . nlp_test/
RUN cd nlp_test/ && \
    python3 -m pip install --no-cache-dir .

CMD ["/bin/bash"]