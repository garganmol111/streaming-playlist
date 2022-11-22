files = $(shell ls)

all:	../project.tar.gz
	@-cd .. && echo "Backup saved at: $(PWD)"

../project.tar.gz:	$(files)
	@-cd .. && tar -zcf project.tar.gz streaming-playlist

clean:
	@-rm -rf ../project.tar.gz && echo "cleaned"