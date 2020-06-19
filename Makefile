build-docker:
	docker build . -t george_floyd:1.0
	docker rm -f george_floyd || true
	docker run --cpus 4 --cpu-shares 1024 --name george_floyd -d -v $(PWD):/app:rw george_floyd:1.0
