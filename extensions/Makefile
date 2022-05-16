## note that this could be cleaned up, e.g. https://github.com/aws-samples/sessions-with-aws-sam/blob/master/swift-custom-runtime/Makefile
## $(eval $@ARTIFACTS_DIR = $(PWD)/.aws-sam/build/ModelMonitorExtension)

build-ModelMonitorExtension:
	$(eval $@ARTIFACTS_DIR = $(PWD)/.aws-sam/build/ModelMonitorExtension)
	mkdir "${ARTIFACTS_DIR}/extensions"
	cp runner "${ARTIFACTS_DIR}/extensions/model-monitor-extension" && \
		chmod +x "${ARTIFACTS_DIR}/extensions/model-monitor-extension"
	cp -R model-monitor-extension "${ARTIFACTS_DIR}/model-monitor-extension"
	cd "${ARTIFACTS_DIR}/model-monitor-extension" && \
		pip3 install -r requirements.txt -t . && \
		chmod +x extension.py
