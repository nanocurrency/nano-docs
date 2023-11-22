FROM squidfunk/mkdocs-material:9.4.10@sha256:01605a03397a654b74b9de3157f56915d1e075e2d3bd22fcf3fb82c443553c25

# Set build directory
#WORKDIR /docs

# Copy files necessary for build
COPY ./ /docs

RUN \
  pip install --upgrade pip && \
  pip install -r /docs/requirements.txt

# Set working directory
WORKDIR /docs

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
