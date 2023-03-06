# Data-Engineering-Project

## Groep 8

- Robin De Waegeneer
- Kyana Marckx
- Levi Matthijs
- Siebe Van Der Donck

## Vragen

### Brussels Airlines
1. Moet de data naar JSON van alle bestemmingen en data in 1 JSON-file of mogen die apart per bestemming?
2. Waar vind je die unike flightkey terug? Is dit verplicht?
3. Als er geen info wordt gegeven (Brussels Airlines) over de vrije plaatsen (dus dit wil zeggen dat er nog genoeg aanwezig zijn), hoe moet dit verwerkt worden? Een lege string of "No information available", ...?
4. Hoe zit het met het formaat van de duration? Mag dit in een string blijven staan of moet het omgezet worden naar minuten in integer, ...?
5. Niet alle bestemming zijn beschikbaar, wat moet er met de bestemming gebeuren waarnaar er niet gevlogen wordt? Moeten die mee in de array met destinations of mag het blijven zoals het nu (dus nergens opgenomen)?