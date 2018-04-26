### ```formatter``` and ```latex_builder```

Formatter allows you to fill templates. It's like .format() but handles absent values. LatexDoc allows you to automatically construct and compile a latex document from python objects.

Here an example of how to use them and how to combine them
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
```

Voilà!

### ```nums_formatters```

This module contains functions to format numerical values.

In particular the function get_str() will allow you to display an ufloat in scientific notaton with a predefined scale. The function will also detect the significant digits. On top it supports units and latex formatting.

Example of usage:

```
>> from uncertainties import ufloat
>> from pyutils.editing.nums_formatters import get_str

>> v = ufloat(100,1.2)
>> get_str(v)
'(10.0 +/- 0.1) x 10^1'
>> get_str(v,scale=4)
'(0.0100 +/- 0.0001) x 10^4'
>> get_str(v,scale=0,otype="latex")
'$100.0 \\pm 1.2$'
>> get_str(v,scale=2,prec=3)
'(1.000 +/- 0.012) x 10^2'
```




