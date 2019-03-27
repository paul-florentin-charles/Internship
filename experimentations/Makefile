install:
	@sudo pip3 install -r requirements.txt

demo:
	@sh demo.sh md=MODE

clean:
	@rm -rf *~ datagen/*~ parser/*~ __pycache__ datagen/__pycache__ parser/__pycache__

cleanall: clean
	@rm -rf dry fx wet info.json

help:
	@echo "INSTALL /w pip: make install"
	#@echo "DEMO: make demo [md=[big/medium/small/tiny]]"
	@echo "DEMO: make demo [md=[long/slow/fast/quick]]"
	@echo "CLEAN: make clean[all]"
