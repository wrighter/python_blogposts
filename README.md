## Python and pandas notebooks

This is a series of notebooks that explore Python, the functionality of [pandas](https://pandas.pydata.org) - the python data analysis and manipulation tool, Python performance, and other topics I've found interesting or helpful.

These correspond to blog posts on [wrighters.io](https://wrighters.io).

For those interested, the method I've used for publishing Jupyter notebooks to Wordpress is to use [pandoc](https://pandoc.org) on the notebook after it's been run and saved. The following arguments work best for me to paste into Wordpress, then I do a little bit of cleanup on the code cells.

```
$ pandoc --wrap=none -f ipynb -t markdown_mmd notebook.ipynb >| output.md
```

