# Zmiany API

## 1.3.1 -> 1.4.0
  
  * Dodanie typu `IDSpecs` w `authorizeUser` (nadmiarowe dane do autoryzacji użytkownika przechowujące właściwości urządzenia i sesji)
  * Dodanie nie-nullowalności w miejscach gdzie nie można do tego dopuścić (zob. `API 1.4.0.md`)
  * Dodanie komentarzy przy polach, które wymagają szerszego opisania ze wględu na ich specyfikę
  * Dodanie komentarzy `# UNUSED` w przypadkach gdy zapytania/pola nie są używanie przez aplikację użytkownika
  * Dodanie możliwości oceniania użytkownikó przez `rankUser` i pobierania swojej aktualnej oceny użytkownika przez `getYourRankOfUser`
  * Zmiana `findUsers` na zupełny interfejs fuzzy-search (większa elastyczność)

## 1.3.0 -> 1.3.1
 
 * Dodanie pola timestamp pod `UserSettings` aby umożliwić wykrywanie nowszych i starszych
konfiguracji stworzony przez użytkownika. Pole jest opcjonalne dla serwera, ale umożliwia lepszą
strategię aktualizacji po stronie klienta w przypadku nie-nullowanych wartości

## 1.2.0 -> 1.3.0:

 * Określenie wymagania na pole `0 <= avgRating <= 1`
 * Przeniesienie `avgRating` i `ratingsNo` do typu `UserProfile` z `User`
 * Zdefiniowanie typu pośredniego trzymającego wyniki zapytania o mecze `MatchSearchResult`
 * Dodanie opcjonalnej obsługi podpowiedzi wyszukiwania `MatchFilterSuggestion`
 * Dodanie ścisłych wymagań nie-nullowalności do wszystkich niezbędnych typów wynikowych

## 1.1.0 -> 1.2.0:
 
 * Dodanie pól `avgRating`, `ratingsNo` w `User`
 * Dodanie typu wyliczeniowego `DisciplineName`
 * Zmiana typu pola `name` w `Category` ze String na `DisciplineName`
 * Dodanie możliwości zresetowania baz danych

## 1.0.0 -> 1.1.0:
 
 * Dodanie pola `title` do meczu
 * Zmiana nazwy pola `long` na `lng`
 * Zmiana typu `timestamp` na String (niezgodność z typem Int)
 * Poprawna zmiana typów na mutacje
 * Zmiana typu `registerUser` z Int na User
 * Poprawka literówki (`mathes`)
 * `registerUser` przyjmuje parametry login, email, hash
 * zmiana `MatchID` na `matchID` (parametry)
 