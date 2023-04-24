# Data-Engineering-Project

## Groep 8

- Robin De Waegeneer
- Kyana Marckx
- Levi Matthijs
- Siebe Van Der Donck

## Vragen

### Algemeen

1. Of er een Done category moet zijn? Ja.

### Brussels Airlines

1. Moet de data naar JSON van alle bestemmingen en data in 1 JSON-file of mogen die apart per bestemming? -> In Orde moet geen Json
2. Waar vind je die unike flightkey terug? Is dit verplicht? -> Moet NIET
3. Als er geen info wordt gegeven (Brussels Airlines) over de vrije plaatsen (dus dit wil zeggen dat er nog genoeg aanwezig zijn), hoe moet dit verwerkt worden? Een lege string of "No information available", ...? -> In Orde
4. Hoe zit het met het formaat van de duration? Mag dit in een string blijven staan of moet het omgezet worden naar minuten in integer, ...? -> _Moet omgezet worden naar INT_
5. Niet alle bestemming zijn beschikbaar, wat moet er met de bestemming gebeuren waarnaar er niet gevlogen wordt? Moeten die mee in de array met destinations of mag het blijven zoals het nu (dus nergens opgenomen)? -> _Geen vluchten beschikbaar_
6. De datatypes van alle waarden (behalve prijs en aantal stops) zijn objecten, zorgt dit voor problemen later of mag het zo blijven? -> In Orde.


ERD: 

![ERD](./images/Schermafbeelding%202023-04-24%20161255.png)


Sterschema:

![Sterschema](./images/Schermafbeelding%202023-04-24%20203049.png)