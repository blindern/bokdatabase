# Bokdatabase Blindern Studenterhjem

Et system for oversikt og katalogisering av bøker på Blindern Studenterhjem!

## Ønsket funksjonalitet

Bokdata:
```
{
	kode: "strekkode for denne oppføringen",
	title: "Tittel på boka",
	subtitle: "Subtittel (hvis den finnes)",
	authors: ["Forfatter 1", "Forfatter 2", ...],
	publishedDate: "Utgivelsesår (kan være dato)",
	description: "Beskrivelse på boka",
	industryIdentifiers: [
		{
			"type": "ISBN_10" eller "ISBN_13" (mulig andre alternativer),
			"identifier": "selve ISBN-nummeret"
		}, ...
	],
	pageCount: antall sider,
	categories: ["kategori 1", "kategori 2", ...],
	deleted: "tidspunkt boka ble fjernet"
}
```

Utlånsdata:
TODO

Use cases:
* Skal kunne registrere bøker ved hjelp av ISBN-kode
* Skal kunne registrere bøker manuelt ved inntasting av felter
* Skal kunne tilordne en registrering mot en egen strekkode
* Skal kunne oppdatere informasjon om bøker, samt markere dem som slettet hvis de kastes
* Skal kunne søke opp bøker ved å søke på tittel og/eller forfatter
* Brukere av biblioteket skal kunne registrere utlån (f.eks. ved hjelp av brukersystemet)
* Brukere skal kunne registrere innlevering av bøker

## Strekkoder
Hver bok på biblioteket får sin egen oppføring i boksystemet. For å enkelt skille mellom bøker får alle bøkene sin egen stekkode med eget nummer. Dette kan brukes for å kjapt identifisere riktig oppføring, samt holde orden på hvilke bøker som er registrert i systemet.

Forslag til format: BSXXXXXX hvor XXXXXX er løpenummer som starter på 000001.

Strekkodeformat: Code 39 mod 43

## Andre ideer
* Ha et felt som holder orden på når bøker sist ble sjekket (scannet)? Da blir det mulig å finne ut hvilke bøker som mangler.