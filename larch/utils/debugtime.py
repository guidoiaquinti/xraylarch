#!/usr/bin/env python

import time
import sys

class debugtime(object):
    def __init__(self, verbose=False, _larch=None, precision=3):
        self._larch = _larch
        self.clear()
        self.verbose = verbose
        self.add('init')

    def clear(self):
        self.times = []

    def _print(self, *args):
        writer = sys.stdout
        if self._larch is not None:
            writer = self._larch.writer
        writer.write(*args)


    def add(self,msg=''):
        if self.verbose:
            self._print(msg, time.ctime())
        self.times.append((msg, time.time()))

    def get_report(self, precision=None):
        if precision is not None:
            self.precision = precision
        prec = self.precision
        m0, t0 = self.times[0]
        tlast= t0
        out = []
        add = out.append
        add("# %s  %s " % (m0,time.ctime(t0)))
        add("#----------------")
        m, tt, dt = 'Message', 'Total' , 'Delta'
        add(f"# {m:32s}    {tt:{prec+2}s}  {dt:{prec+2}s}")
        for m,t in self.times[1:]:
            tt = t-t0
            dt = t-tlast
            if len(m)<32:
                m = m + ' '*(32-len(m))
            add(f"  {m:32s}    {tt:.{prec}f}  {dt:.{prec}f}")
            tlast = t
        add('')
        return "\n".join(out)

    def show(self, precision=None):
        self._print(self.get_report(precision=precision))

    def save(self, fname='debugtimer.dat'):
        dat = self.get_report()
        with open(fname, 'w') as fh:
            fh.write('%s\n' % dat)

def debugtimer(_larch=None):
    """debugtimer returns a Timer object that can be used
    to time the running of portions of code, and then
    write a simple report of the results.  the Timer object
    has methods:

      clear()   -- reset Timer
      add(msg)  -- record time, with message
      show_report -- print timer report

    An example:

      timer = debugtimer()
      x = 1
      timer.add('now run foo')
      foo()
      timer.add('now run bar')
      bar()
      timer.show_report()
    """
    return debugtime(_larch=_larch)
