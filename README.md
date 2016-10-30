# zswap

A replacement to `#include` that can be used in any file

## Syntax

To include a file into another file you can use a **zswap tag** :

`#&zwap<path/to/file>`

(If you don't like `#&`, you can also use your own prefix)

## Usage

`zswap :options files`

You can also type `zswap` to show the help

## Options

In `zswap`, options start with `:`

- `:override` / `:overwrite` : Overwrite the file with the result

- `:no-output` : Doesn't show the result

- `:no-errors` : Doesn't show any errors

- `:no-warnings` : Doesn't show any warnings

- `:zold` : Create a backup file with the `.zold` extension (Automatically enable `:override` if the `.zold` file could be created)

- `:zfile` : Write the result to a file with the `.zfile` extension

- `:prefix=?` : Set a custom prefix (Here, the custom prefix is `?`)

- `:escape=?` : Escape a string in included files (Here, the escaped string is `?`)

- `:help=?` : Show an option's help (Here, the option is `?`) (eg : `zswap :help=override`)

## Dependancies

You need to have `python` installed to use this script

