# `szkopul-submit`

Nieoficjalny program do przesyłania rozwiązań do serwisu [Szkopuł](https://szkopul.edu.pl/) przez API.

## Instalacja

Najuniwersalniejszą i jedną z najłatwiejszych metod instalacji jest użycie [pipx](https://pipx.pypa.io/stable/how-to/install-pipx.html).

```bash
pipx install https://github.com/bartekl1/szkopul-submit/releases/download/v1.0.0/szkopul_submit-1.0.0-py3-none-any.whl
```

## Używanie

### Inicjacja folderu z rozwiązaniami

Należy przygotować folder, w którym będą przechowywane rozwiązania do danego konkursu.

W folderze należy wykonać polecenie `szkopul-submit --init`, a następnie podać [token API](https://szkopul.edu.pl/api/token) i nazwę konkursu.

Zostanie utworzony plik `szkopul.config.json`.

Można teraz przesyłać rozwiązania.

> [!CAUTION]
> Plik `szkopul.config.json` zawiera token API.

### Przesyłanie rozwiązań

Aby przesłać rozwiązanie należy wykonać polecenie:

```bash
szkopul-submit abc.cpp
```

Program automatycznie wykrywa nazwę zadania z nazwy pliku jeśli jest ona w formacie `xxx.yyy` lub `xxx123.yyy`, gdzie `xxx` to trzyliterowy kod zadania, `123` to dowolna liczba naturalna (opcjonalne), a `yyy` to rozszerzenie spośród `.cpp`, `.c` i `.py`.

Jeśli nazwa pliku nie jest zgodna z tym formatem, można ręcznie wskazać zadanie za pomocą parametru `-p` lub `--problem`, np.:

```bash
szkopul-submit zadanie.cpp --problem abc
```

### Pomoc

Aby uzyskać pomoc, należy uruchomić program z argumentem `-h` lub `--help`.

```bash
szkopul-submit --help
```

## Licencja

Program publikowany jest na licencji [MIT](LICENSE).
