from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from random import randint
import os.path
import math

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

def createPdf(barcodes, sizes, copies=1, outfile="barcodes.pdf", drawRect=False):
    c = canvas.Canvas(outfile, pagesize=A4)

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
    maxPerPage = math.floor((sizes['nx'] * sizes['ny']) / copies) * copies
    currentCountOnPage = 0    
    for item in barcodes:
        for entry in range(copies):
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
            currentCountOnPage += 1
            cy-=1
            if cy < 0 or currentCountOnPage == maxPerPage:
                if cx == sizes['nx']-1 or currentCountOnPage == maxPerPage:
                    # new page
                    c.showPage()
                    firstOnPage = True
                    currentCountOnPage = 0
                    cx = 0
                    cy = sizes['ny']-1
                else:
                    cy = sizes['ny']-1
                    cx += 1

    c.save()

def saveBarcodes(filename, list):
    with open(filename, 'w') as f:
        f.write('\n'.join(list))

def getBarcodes(filename):
    if not os.path.isfile(filename):
        return []

    list = []
    with open(filename, 'r') as f:
        for line in f.read().split('\n'):
            if line.strip() != "":
                list.append(line.strip())
    return list

def getBarcodesNumberMap(barcodes_full):
    barcodes_map = {}
    for barcode in barcodes_full:
        if barcode[0:3] != 'BS-':
            raise Exception('Invalid barcode: %s' % barcode)
        barcodes_map[int(barcode[3:-3], 16)] = barcode
    return barcodes_map

def makeBarcodes(start, count):
    barcodes = []
    for x in xrange(start, start+count):
        code = "BS-%04X-%02X" % (x, randint(0, 255))
        barcodes.append(code)
    return barcodes

