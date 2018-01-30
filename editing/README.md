#### ```formatter``` and ```latex_builder```

You can use this object to automatically build latex from templates and compile it.

Here an example
```
from pyutils.editing import PartialFormatter as Formatter
from pyutils.editing import latex_doc

fmt = Formatter()
table = fmt.format(open(loc.TEPLATES+"table_template.txt").read(),**results)

latex = latex_doc(loc.TABLES+"/table.tex")
latex.set_title("My cool title")
latex.add_to_preamble(loc.LHCB+"/preamble.tex")
latex.add_to_preamble(loc.LHCB+"/lhcb-symbols-def.tex")
latex.insert_line("Inserts some explanation: main text of the latex")
latex.insert_figure(glob.glob(loc.PLOTS+"*.pdf"),ninrow=2)
latex.insert_tabular(table,"Some nice caption")
latex.close_and_compile()
```
