all: clean
	QT5DIR=/usr/lib/x86_64-linux-gnu/qt5 python2 -m PyInstaller -F \
	--hidden-import pyjvmo.jvmo \
	--add-data gui/qml:gui/qml \
	java.py

clean:
	rm -rf dist
	rm -rf build
	find . -name "*.qmlc" -type f -delete
	find . -name "*.pyc" -type f -delete
	find . -name "*.spec" -type f -delete