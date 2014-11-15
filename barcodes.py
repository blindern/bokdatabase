from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from random import randint

sizes = {
    # Herma 10901
    10901: {
        # first box offset
        'x0': 11.02 * mm,
        'y0': 13.06 * mm,

        # box size
        'w': 35.56 * mm,
        'h': 16.93 * mm,

        # space between
        'ox': 2.54 * mm,
        'oy': 0,

        # count in each axes
        'nx': 5,
        'ny': 16,

        # element offsets
        't0y': 12*mm,
        't1y': 3*mm,
        'by': 5*mm,

        # barcode height
        'bh': 6*mm
    },

    # Herma 8337
    8337: {
        # first box offset
        'x0': 6.5 * mm,
        'y0': 14.8 * mm,

        # box size
        'w': 37 * mm,
        'h': 13 * mm,

        # space between
        'ox': 3 * mm,
        'oy': 2.97 * mm,

        # count in each axes
        'nx': 5,
        'ny': 17,

        # element offsets
        't0y': 13*mm-3.7*mm,
        't1y': 1.8*mm,
        'by': 3.7*mm,

        # barcode height
        'bh': 5*mm
    }
}

def createBarCodes(barcodes, sizes, drawRect=False):
    c = canvas.Canvas("barcodes.pdf", pagesize=A4)
    
    # first box offset
    x0 = sizes['x0']
    y0 = sizes['y0']

    # box size
    w = sizes['w']
    h = sizes['h']

    # extra space between
    ox = sizes['ox']
    oy = sizes['oy']

    firstOnPage = True
    cx = 0
    cy = sizes['ny']-1
    for item in barcodes:
        # draw rectangles for debugging
        if firstOnPage and drawRect:
            firstOnPage = False
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(.5)
            
            for yi in xrange(sizes['ny']):
                for xi in xrange(sizes['nx']):
                    c.rect(x0+xi*(w+ox), y0+yi*(h+oy), w, h)

        barcode128 = code128.Code128(item, barHeight=sizes['bh'])
        barcode128.drawOn(c, x0+cx*(w+ox)-2*mm, y0+cy*(h+oy)+sizes['by'])

        c.setFont("Helvetica", 6)
        c.drawCentredString(x0+cx*(w+ox)+w/2, y0+cy*(h+oy)+sizes['t0y'], "Biblioteket Blindern Studenterhjem")

        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(x0+cx*(w+ox)+w/2, y0+cy*(h+oy)+sizes['t1y'], item)

        # find next position
        cy-=1
        if cy < 0:
            if cx == sizes['nx']-1:
                # new page
                c.showPage()
                firstOnPage = True
                cx = 0
                cy = sizes['ny']-1
            else:
                cy = sizes['ny']-1
                cx += 1

    c.save()

if __name__ == "__main__":
    size = sizes[10901]

    #start = 0x50+1
    start = 1
    count = size['nx'] * size['ny'] * 2 / 2;
    repeats = range(2)
    
    barcodes = []
    for x in xrange(start, start+count):
        code = "BS-%04X-%02X" % (x, randint(0, 255))
        for repeat in repeats:
            barcodes.append(code)

    createBarCodes(barcodes, size, drawRect=True)