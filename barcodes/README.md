# Barcodes til biblioteket Blindern Studenterhjem

Denne mappen består av scripts for å generere barcodes-serier og utskriftbar PDF
med barcodes.

Generere barcodes:
`./cli.py --start 100 --count 40 generatecodes`

Produsere PDF-fil:
`./cli.py --start 100 --count 40 generatepdf

Barcodes lagres som standard i barcodes.txt og barcodes.pdf. Barcodes legges til i lista,
slik at ikke tidligere opprettede oppføringer slettes.

## Ark for barcodes
Vi har kjøpt HERMA nr 8337 som barcodes er skrevet ut på. Disse er plastbelagte og
viser seg å passe ganske bra. Vi har kjøpt disse gjennom nortea.no.

Utskriftstips:
* Sett papirtype til `Extra Heavy 131-175`
* Pass på så det ikke skrives ut dobbelt
* Skriv ut i 100 % (ikke skaler)
* Gjør en test på vanlig ark først og se om rutene passer

## Status
* Per 15. november 2014 var det skrevet ut barcodes opp til og med BS-03A4-07 (932).
* 4. november 2015 ble det skrevet ut 50 ark med barcodes opp til og med BS-0B48 (3032).
  Dette ble fordelt over 2 x 25 ark (altså 2 sett med 8337-lapper). Det er etter dette
  ingen flere blanke lapper igjen, og det må kjøpes inn mer når man må trykke opp flere.

## Andre tips

### Sjekke brukte koder i databasen
```bash
mongo intern -u laravel -p
```

Passord hentes fra `/var/www/aliases/intern/.env.php`

```
db.books.find({$query: {}, $orderby: {bib_barcode: -1}}, {bib_barcode: 1})
```

