'''
Module that defines class MultiCanvas, to draw multiple drawables in the same canvas
'''

import ROOT as r
import itertools


class MultiCanvas:
    '''
    Drawables is a list of lists of drawbles es
    [[d1, d2], [d3, d4]] and it will plot

    ----------
    | d1  d2 |
    | d3  d4 |
    ----------

    the drawable can also be a tuple (drawable, option string to Draw)
    '''

    def __init__(self, drawables):
        # replace single line: [d1, d2] -> [[d1, d2]]
        try:
            drawables[0][0]
        except TypeError:
            drawables = [drawables]
        self.drawables = drawables

    def Draw(self, canvas):
        nx = max([len(i) for i in self.drawables])
        ny = len(self.drawables)
        canvas.Clear()
        canvas.Divide(nx, ny)

        for i, j in itertools.product(range(nx), range(ny)):
            canvas.cd(ny*i+j+1)
            try:
                drawable = self.drawables[i][j]
                try:
                    drawable, opts = drawable
                except (ValueError, TypeError):
                    opts = ''
                if 'colz' in ''.join([str(i) for i in opts]): # works both for a single string or a list of options
                    r.gPad.SetRightMargin(0.15)
                if 'logz' in ''.join([str(i) for i in opts]): # works both for a single string or a list of options
                    r.gPad.SetLogz()
                if isinstance(opts, str):
                    drawable.Draw(opts)
                else:
                    drawable.Draw(*opts)
            except IndexError:
                pass
        canvas.cd(0)

# test
if __name__ == '__main__':

    c = r.TCanvas()

    h1 = r.TH1D('h1', 'h1', 10, 0,10)
    for i in range(5):
        h1.Fill(i)

    h2 = r.TH1D('h2', 'h2', 10, 0,10)
    for i in range(5,10):
        h2.Fill(i)

    h3 = r.TH2D('h3', 'h3', 10, 0,10, 10, 0, 10)
    for i in range(5):
        for j in range(5,10):
            h3.Fill(i,j)


    mc = MultiCanvas([[h1,h2],[(h3,'colz')]])
    mc.Draw(c)

    c.Update()
