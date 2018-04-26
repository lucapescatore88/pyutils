#### ```formatter``` and ```latex_builder```

You can use this object to automatically build latex from templates and compile it.

Here an example
```
from pyutils.editing import PartialFormatter as Formatter
from pyutils.editing import LatexDoc

## Formatter allows you to fill templates. It's like .format() but handles absent values
fmt = Formatter()
table = fmt.format(open("table_template.txt").read(),**results)

## LatexDoc allows you to automatically construct and compile a latex document from python objects.
latex = LatexDoc("table.tex")
latex.set_title("My cool title")
latex.add_to_preamble("preamble.tex") e.g. Add lhcb symbols!!
latex.insert_line("Inserts some explanation: main text of the latex")
latex.insert_figure(glob.glob(loc.PLOTS+"*.pdf"),ninrow=2)
latex.insert_tabular(table,"Some nice caption") # "table" is a string e.g. from a template
latex.insert_list(["item1","item2"],"Some nice caption")
latex.close_and_compile()

Voilà!
```
