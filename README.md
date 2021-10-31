# Social Network Visualiser (snvis)

This is a tool to visualise social networks from a spreadsheet of connections.

## Installing

```sh
pip install snvis
```

Python 3.9 or greater is required.

## Usage

Once you have installed `snvis`, you can run it using `snvis` as long as you
have added the directory it was installed to to your path. If this doesn't work,
you can run:

```sh
python -m snvis
```

The only required argument is the spreadsheet to parse, in tab-separated values
format.

An example usage would be:

```sh
snvis data.tsv -v
```

This runs on the file `data.tsv` in verbose mode so that you can see what the
program is doing.

To see all options, run:

```sh
snvis -h
```

## Contributing

### Commits

When writing commit messages, please use conventional commits.

### Building

To build a release, install build using 

```sh
pip install build
```

then to build the package, run

```sh
python -m build
```