#!/usr/bin/env python3

from barcodes_lib import *
import sys
import getopt

def usage():
    print('Usage:')
    print('%s --start 123 --count 40 generatecodes' % sys.argv[0])
    print('%s --start 123 --count 40 generatepdf' % sys.argv[0])
    print('Options:')
    print('  --codes barcodes.txt   Override file to read/write known barcodes numbers')
    print('  --output barcodes.pdf  Override file to write PDF with barcodes')

def generateCodes(codesfile, startNumber, count):
    if startNumber < 0:
        raise Exception("Startnumber cannot be negative")
    if count <= 0:
        raise Exception("Count must be greater than zero")

    barcodes = getBarcodes(codesfile)
    existing = getBarcodesNumberMap(barcodes)

    if len(existing) > 0:
        if max(existing) + 1 != startNumber:
            print('When using existing codes file, start number must continue the list')
            print('Next available number: %d' % (max(existing) + 1))
            sys.exit(3)

        for num in xrange(startNumber, startNumber + count):
            if num in existing:
                print('Number %d is already in list. Next available number: %d' % (num, max(existing)+1))
                sys.exit(3)

    barcodes = barcodes + makeBarcodes(startNumber, count)
    saveBarcodes(codesfile, barcodes)
    
    print('Generated %d barcodes' % count)

def generatePdf(codesfile, startNumber, count, outfile):
    size = sizes[8337]
    copies = 2

    barcodesFullList = getBarcodes(codesfile)
    numberMap = getBarcodesNumberMap(barcodesFullList)

    barcodes = []
    for num in xrange(startNumber, startNumber + count):
        if not num in numberMap:
            print('Number %d (count = %d) not found in barcodes file' % (num, num - startNumber))
            print('%s contains %d entries' % (codesfile, len(barcodesFullList)))
            print('Perhaps you need to create some barcodes first?')
            sys.exit(3)
        barcodes.append(numberMap[num])

    createPdf(barcodes, size, copies=copies, outfile=outfile, drawRect=False)
    print('Generated pdf for %d barcodes' % count)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "", [
            'start=',
            'count=',
            'codes=',
            'outfile='
        ])
    except:
        usage()
        sys.exit(2)

    start = 0
    count = 0
    codesfile = 'barcodes.txt'
    outfile = 'barcodes.pdf'

    for opt, arg in opts:
        if opt == '--start':
            start = int(arg)
        elif opt == '--count':
            count = int(arg)
        elif opt == '--codes':
            codesfile = arg
        elif opt == '--output':
            outfile = arg

    if len(args) == 0:
        usage()
        sys.exit(2)

    if args[0] == 'generatecodes':
        generateCodes(codesfile, start, count)

    elif args[0] == 'generatepdf':
        generatePdf(codesfile, start, count, outfile)

    else:
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
