[RAPORT.md](https://github.com/user-attachments/files/33977207/RAPORT.md)
# Projekt 1, świat klocków (na 4 pkt)

Python 3, bez dodatkowych bibliotek.

```
python3 klocki.py przyklady/przyklad.txt
python3 eksperymenty.py
python3 -m unittest discover -s tests -v
```

- `klocki.py` - cały program: klasa `Uklad`, wczytywanie, DFS, weryfikacja
- `eksperymenty.py` - losowe problemy z zadania 4, wyniki w `wyniki.md`
- `przyklady/` - przykład z treści i 4 pliki ze złymi układami
- `tests/` - kilka testów

## Zadanie 1

Układ to klasa `Uklad`. Trzyma krotkę `pod`, gdzie `pod[k-1]` to klocek, na którym leży
klocek k (0 to stół), czyli to samo co w pliku. Klocek jest wolny, jeśli jego numeru nie ma
w `pod`.

Funkcja `blad_ukladu` sprawdza, czy klocek nie leży na sobie, na klocku którego nie ma,
czy na jednym klocku nie leżą dwa i czy nie ma cyklu. Cykl sprawdzam tak: od każdego klocka
schodzę w dół N razy. Jak dalej nie jestem na stole, to musiałem chodzić w kółko.

## Zadanie 2

DFS jest rekurencyjny. Z danego układu próbuje po kolei ruchów. Jak ruch prowadzi do nowego
układu, wchodzi w niego. Jak stamtąd nie da się dojść do celu, cofa ruch (`sciezka.pop()`)
i próbuje następnego. To jest nawrót.

Odwiedzone układy są w secie, więc żaden nie jest odwiedzany dwa razy i nie ma pętli.
Limit: 1 000 000 rozwiniętych węzłów albo 60 sekund. Jak się przekroczy, program wypisuje
`Przekroczony limit węzłów albo czasu`.

Kolejność ruchów (funkcja `kolejnosc`). Klocek jest na miejscu, jeśli leży tam gdzie w celu
i wszystko pod nim też. Najpierw próbuję ruchów, które kładą klocek od razu na jego docelowe
miejsce (na stół albo na klocek, który już jest na miejscu). Potem zdejmowanie na stół
klocków, które leżą źle. Na końcu cała reszta.

Z taką kolejnością DFS robi po prostu: rozbierz to, co stoi źle, i buduj wieże od dołu.
Zawsze jest jakiś ruch z pierwszej albo drugiej grupy, więc DFS nigdy się nie cofa, a każdy
klocek rusza się najwyżej 2 razy (na stół i na miejsce).

## Zadanie 3

`weryfikuj` robi ruchy po kolei i sprawdza: czy klocek istnieje, czy nie kładziemy go na
sobie, czy jest wolny, czy nie kładziemy na stół czegoś, co już na nim leży, czy klocek pod
spodem jest wolny i czy nie przekładamy z klocka na klocek. Na końcu porównuje wynik z celem.
Zwraca `OK` albo np. `błąd w ruchu nr 2: klocek 1 nie jest wolny`.

## Zadanie 4

Ziarno 2026, po 5 problemów dla N od 3 do 15. Układ losuję tak: klocki w losowej kolejności,
każdy na stół albo na górę którejś wieży. Cała tabela i ruchy dla N do 8 są w `wyniki.md`.

| N | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| średnio ruchów | 2,0 | 2,6 | 5,2 | 5,8 | 7,6 | 8,8 | 11,2 | 12,8 | 13,4 | 15,2 | 14,8 | 17,8 | 20,2 |

Wszystkie 65 problemów rozwiązane i wszystkie przeszły weryfikację. Węzłów zawsze tyle co
ruchów (zero nawrotów), czas poniżej 1 ms. Przykład z treści daje 7 ruchów, czyli tyle,
ile wynosi najkrótsza sekwencja. Ogólnie algorytm nie gwarantuje najkrótszej, ale na 4 pkt
nie trzeba.
