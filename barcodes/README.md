# Barcodes til biblioteket Blindern Studenterhjem

Denne mappen består av scripts for å generere barcodes-serier og utskriftbar PDF
med barcodes.

Generere barcodes:
`./cli.py --start 100 --count 40 generatecodes`

Produsere PDF-fil:
`./cli.py --start 100 --count 40 generatepdf

Barcodes lagres som standard i barcodes.txt og barcodes.pdf. Barcodes legges til i lista,
slik at ikke tidligere opprettede oppføringer slettes.

## Status
Per 15. november 2014 var det skrevet ut barcodes opp til BS-03A4-07.


