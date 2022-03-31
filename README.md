# Kompilatory

## Opis

Kompilator dla prostego języka bazującego na składni Matlaba wykorzystywanego dla operacji macierzowych. Zbudowany na bibliotece lex/yacc. 

## Funkcje

- Analiza leksykalna - podział pliku wejściowego na tokeny i odpowiadające mu leksemy. Skaner pomija białe znaki i komentarze. Zwracany jest ciąg tokenów, 
który potem przyjmowany jest przez parser. Jeśli nie uda się wyodrębnić tokenu, sygnalizowany jest błąd leksykalny.
- Analiza składniowa - budowany jest parser na podstawie reguł gramatyki języka, który rozpoznaje tokeny i sygnalizuje błędy składniowe.
- Analiza sematyczna - sprawdzenie poprawności konstrukcji analizując drzewa syntaktyczne. Zajmuje się m. in. kontrolą zgodności typów przy operacjach
arytmetycznych i macierzowych oraz zakresu osiągalności zmiennych.
- Interpreter - przechowuje w pamięci zmienne programu, pozwala na wykonanie kodu. Pozwala na odczyt i zapis do zmiennych oraz referencji.

## Materiały

https://home.agh.edu.pl/~mkuta/tklab/

## Uruchomienie

Do uruchomienia potrzebne jest środowisko Pythona w wersji minimum 3.8.

Konieczna jest także biblioteka lex/yacc.

``` pip install ply  ```

W głównym katalogu programu należy wywołać 

``` python src/main.py [ścieżka do pliku z kodem]  ```

## Informacje

Przykładowe programy do wywołania zostały umieszczone w folderze [scripts](https://github.com/t0ms0n00/Kompilatory/tree/main/scripts).

## Autorzy

#### Paweł Lewkowicz 

#### Tomasz Boroń
