# noto - A non-deterministic note box

noto is a small CLI application, that allows you to very quickly store and edit notes on your local machine
and read them again at your leisure.

You can **prioritize** and **tag** your notes, as well as **update** and **delete** them. The application is designed to be as fast and simple to use on the command line.

## Installation

## Examples

### Creating a Note

``` bash
noto write "Hello World!"
> Note(id=1, text=Hello World!)
```

You may also assign a priority and/or tags on creation:

``` bash
noto write "Hello Moon!" -p 9000 -t foo -t bar
> Note(id=2, text=Hello Moon!, priority=9000, tags=[foo, bar])
```

### Interactive Mode

noto is designed to make it easy for you to journal through a stream of random notes.

> You can configure the behaviour of the interactive mode - including whether to return highest prio notes instead of random ones - by editing the `config.yaml`.

To get started, do this:

``` bash
noto
```

You will be presented with a random note that you've written in the past.

``` bash
Note(id=512, text=Whazzup?)
```

In addition, you will be presented with options to modify that note:

``` bash
Modifying note: Confirm (Enter), Content (c), Priority (p), Remove Tag (t), Add Tag (T), Delete Note (D), Quit (q)
```

### Manual Mode

As an alternative, you can edit your notes as well using specific commands:

``` bash
noto write
```

``` bash
noto read
```

``` bash
noto update
```

``` bash
noto delete
```

See their respective `--help` commands for further information.