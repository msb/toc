# Table of Contents Generation (TOC)

I maintain a number of different songbook PDFs the source of which are typically a folder
containing a set of mostly single page PDFs for each song.
I use [`pdftk`](https://www.pdflabs.com/docs/pdftk-cli-examples/) to compile these song
files into the songbook. However I would like to generate a table of contents listing the songs and
their page numbers to be included in the songbook. This python script meets that requirement by
consuming the list of song files, using the file names as the song titles, and outputing a set of
TOC PDFs to the same folder.

The script makes certain assumptions about the structure of the song filenames. These assumptions
along with tool's general usage are detailed in the script's help. You can access this help by
running

```sh
docker run --rm msb140610/toc:$VERSION --help
```

```powershell
docker run --rm msb140610/toc:$env:VERSION --help
```

Note that the current version is

```sh
VERSION=0.2
```

```powershell
$env:VERSION=0.2
```

Note also that a [Docker compose script project](https://github.com/msb/compile-songbook) has been
created that orchestrates songbook creation using this project, along with
[`rclone`](https://rclone.org/) and [`pdftk`](https://www.pdflabs.com/docs/pdftk-cli-examples/).

## Development

Change requests are welcomed for this project. Once you have checked out the project and made your
changes, to test these changes locally before you make the CR you can run the script with docker
using

```sh
docker run --rm -u $(id -u):$(id -g) -v $PWD:/app msb140610/toc:$VERSION /app/example
```

```powershell
docker run --rm -v ${pwd}:/app msb140610/toc:$env:VERSION /app/example
```

This will run the script against the song files in the local `example` sub-folder
and output the TOC pdf in the same folder.

Alternatively, if you are making dependency changes, you can build your own docker image using

```sh
docker build -t toc-dev .
```

.. and then run the script using

```sh
docker run --rm -u $(id -u):$(id -g) -v $PWD:/app toc-dev /app/example
```

```powershell
docker run --rm -v ${pwd}:/app toc-dev /app/example
```

To maintain code quality you should also run [`mypy`](https://mypy.readthedocs.io/en/stable/) and
[`flake8`](https://flake8.pycqa.org/en/latest/) to check for warnings/errors as follows

```sh
docker run --rm --entrypoint flake8 -v $PWD:/app toc-dev

docker run --rm --entrypoint mypy -v $PWD:/app toc-dev *.py
```

```powershell
docker run --rm --entrypoint flake8 -v ${pwd}:/app toc-dev

docker run --rm --entrypoint mypy -v ${pwd}:/app toc-dev .
```
