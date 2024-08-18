# Define a rule for cleaning previous builds
clean:
	@echo "Cleaning up old distribution files..."
	rm -rf build/ dist/ *.egg-info

# Define a rule for building the distribution files
build: clean
	@echo "Building source distribution and wheel..."
	python setup.py sdist bdist_wheel

# Define a rule for uploading the package to PyPI
upload: build
	@echo "Uploading the package to PyPI..."
	twine upload dist/*

# Define a rule that performs all steps
release: clean build upload
	@echo "Release complete!"
