all: filelist.tex svninfo.tex

svninfo.tex:
	svn info ../../../ | egrep "(Revision:|URL:)" > svninfo.tex

filelist.tex:
	./generate_filelist > filelist.tex

clean:
	rm svninfo.tex
	rm filelist.tex
