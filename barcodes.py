from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from random import randint

#----------------------------------------------------------------------
def createBarCodes(barcodes, drawRect=False):
    c = canvas.Canvas("barcodes.pdf", pagesize=A4)
    
    # first box offset
    x0 = 11.02 * mm
    y0 = 13.06 * mm

    # box size
    w = 35.56*mm
    h = 16.93*mm

    # extra space between
    ox = 2.54*mm
    oy = 0

    # draw rectangles for debugging
    if drawRect:
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(.5)
        for yi in xrange(16):
            for xi in xrange(5):
                c.rect(x0+xi*(w+ox), y0+yi*(h+oy), w, h)

    cx = 0
    cy = 15
    for item in barcodes:
        barcode128 = code128.Code128(item)
        barcode128.drawOn(c, x0+cx*(w+ox)-2*mm, y0+cy*(h+oy)+5*mm)

        c.setFont("Helvetica", 6)
        c.drawCentredString(x0+cx*(w+ox)+w/2, y0+cy*(h+oy)+h-4*mm, "Biblioteket Blindern Studenterhjem")

        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(x0+cx*(w+ox)+w/2, y0+cy*(h+oy)+2*mm, item)

        # find next position
        cy-=1
        if cy < 0:
            cy = 15
            cx += 1

    c.save()

if __name__ == "__main__":
    start = 1
    count = 16*5/2
    repeats = range(2)

    barcodes = []
    for x in xrange(start, start+count):
        code = "BS-%04X-%02X" % (x, randint(0, 255))
        for repeat in repeats:
            barcodes.append(code)

    createBarCodes(barcodes, drawRect=True)