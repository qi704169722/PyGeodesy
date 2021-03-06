
# -*- coding: utf-8 -*-

# Test wgrs module.

__all__ = ('Tests',)
__version__ = '19.05.07'

from base import TestsBase

from pygeodesy import degDMS, fStr, Georef, S_DEG, S_MIN, wgrs


def _fStr(floats, prec=6):
    return ', '.join('None' if f is None else fStr(f, prec=prec) for f in floats)


class Tests(TestsBase):

    def testCodec3(self, g, x, prec=4):
        self.test('codec3', Georef(g), g)
        t = wgrs.decode3(g)
        self.test('decode3', _fStr(t, prec=prec), x)
        self.test('encode', wgrs.encode(*t), g)

    def testCodec5(self, g, x, prec=4):
        self.test('codec5', Georef(g), g)
        t = wgrs.decode5(g)
        self.test('decode5', _fStr(t, prec=prec), x)
        self.test('encode', wgrs.encode(*t), g)

    def testGeoref(self, LL):

        # Karney's geographiclib/1.49/examples/example-Georef.cpp
        # <https://SourceForge.net/p/geographiclib/code/ci/release/tree/examples/example-Georef.cpp>
        g = Georef('57.64911, 10.40744', precision=6)
        self.test('Georef', g, 'NKLN2444638946')
        self.test('Georef', repr(g), "Georef('NKLN2444638946')")
        self.test('Georef.latlon', fStr(g.latlon, prec=5), '57.64911, 10.40744')
        t = g.toLatLon(LL)
        self.test('Georef.toLatLon', repr(t), 'LatLon(57°38′56.8″N, 010°24′26.78″E)')
        self.testCodec3(g, '57.64911, 10.40744, 6.0', prec=5)

        # <https://WikiPedia.org/wiki/World_Geographic_Reference_System>
        g = Georef('38.286108, -76.4291704', precision=6)
        self.test('Georef', g, 'GJPJ3424917166')
        self.test('Georef', repr(g), "Georef('GJPJ3424917166')")
        self.test('Georef.latlon', fStr(g.latlon, prec=6), '38.286108, -76.42917')
        t = g.toLatLon(LL)
        self.test('Georef.toLatLon', repr(t), 'LatLon(38°17′09.99″N, 076°25′45.01″W)')
        self.testCodec3(g, '38.286108, -76.429175, 6.0', prec=6)

        # <https://Earth-Info.NGA.mil/GandG/coordsys/grids/georef.pdf>
        self.testCodec3('MKPG1204', '51.075, -1.7917, 3.0', prec=4)

        # <https://www.Map-Reading.com/ch4-4.php>
        self.testCodec3('WJKG1503', '36.0583, 129.2583, 3.0', prec=4)

        # <https://WikiPedia.org/wiki/World_Geographic_Reference_System>
        self.testCodec5('GJPJ4103R5',    '38.0583, -76.3083, 3.0, None, 9260.0',   prec=4)
        self.testCodec5('GJPJ4103H17',   '38.0583, -76.3083, 3.0, 5181.6, None',   prec=4)
        self.testCodec5('GJPJ4103R5H17', '38.0583, -76.3083, 3.0, 5181.6, 9260.0', prec=4)

        for t in range(-1, 13):
            r = wgrs.resolution(t)
            p = wgrs.precision(r)
            self.test('precision', t, p, known=t < 0 or t > 11)
            b = degDMS(r, prec=t if r < 1 else 0, s_S='')  # no S_SEC
            x = ('15' + S_DEG) if p < 1 else (
                ( '1' + S_DEG) if p < 2 else ('0.%s1%s' % ('0' * (p - 2), S_MIN)))
            self.test('resolution', b, x)  # also to test degDMS


if __name__ == '__main__':

    from pygeodesy import ellipsoidalVincenty

    t = Tests(__file__, __version__, wgrs)
    t.testGeoref(ellipsoidalVincenty.LatLon)
    t.results()
    t.exit()
