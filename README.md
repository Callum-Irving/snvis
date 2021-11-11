# Social Network Visualiser (snvis)

This is a tool to visualise social networks from a spreadsheet of connections.
It creates an svg image and then displays is with the default system tool.

Example:

![demo image](https://raw.githubusercontent.com/Callum-Irving/snvis/5447bdaf3702e0233885c4e501c056e8a5463655/example/graph.svg?raw=true)

## Installing

Requirements:
* xdg-open (Linux only)
* Python 3.9 or greater

```
pip install snvis
```

or if you want the latest development version (recommended):

```
pip install git+https://github.com/Callum-Irving/snvis.git#egg=snvis
```

## Usage

Once you have installed `snvis`, you can run it using `snvis` as long as you
have added the directory it was installed to to your path. If this doesn't work,
you can run:

```
python -m snvis
```

The only required argument is the spreadsheet to parse, in tab-separated values
format.

An example usage would be:

```
snvis data.tsv --view
```

This runs on the file `data.tsv` in verbose mode so that you can see what the
program is doing.

To see all options, run:

```
snvis -h
```

### Data Structure

The data for the network should be in a *.tsv file. In this file, one column
should contain the name for each person in the network and a second column
should contain the names of all other people that the person is connected to.
Connections can go both ways or just one, right now they are the same.

Example spreadsheet:

| name    | connections   |
| -----   | ------------- |
| James   | Robert, John  |
| Michael |	Wiliam, David |
| Roberf  | John          |
| William | David, Robert |
| David   | Michael       |
| John    | James, roberf |

Notice that there are some typos in this spreadsheet. The program can detect
minor typos like "Roberf". The program uses the names in the "name" column as
the correct names. In this example "Robert" would actually get corrected to
"Roberf" because "Robert" is only in the "connections" column and "Roberf" is in
the "name" column.

## Contributing

### Commits

When writing commit messages, please use conventional commits.

### Building

To build a release, run

```
python setup.py sdist bdist_wheel
```
