from python:alpine
# ENV apiurl
# ENV jwt
# ENV fileid
# ENV gitrepo
# ENV packagepath
# ENV loglevel

RUN addgroup -S openiapgroup && adduser -S openiapuser -G openiapgroup

USER openiapuser
WORKDIR /home/openiapuser
RUN pip install grpcio openiap
COPY --chown=openiapuser:openiapgroup src/agent.py /home/openiapuser
CMD [ "python", "/home/openiapuser/agent.py" ]

# docker buildx build --platform linux/amd64 -t openiap/pyagent:latest . --load