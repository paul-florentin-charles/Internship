install:
	@sudo pip3 install -r requirements.txt

demo: 
	@./demo.py 

clean:
	@rm -rf *~ datagen/*~ parser/*~ __pycache__ datagen/__pycache__ parser/__pycache__

cleanall: clean
	@rm -rf dry fx wet info.json

help:
	@echo "INSTALL /w pip: make install"
	@echo "DEMO: make demo"
	@echo "CLEAN: make clean[all]"
