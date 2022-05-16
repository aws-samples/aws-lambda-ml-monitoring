FROM python:3.8-alpine AS installer
#Layer Code

COPY .aws-sam/build/ModelMonitorExtension /opt
WORKDIR /opt/model-monitor-extension
RUN chmod +x extension.py


FROM scratch AS base
WORKDIR /opt
COPY --from=installer /opt .
