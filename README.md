# congreso_chile
Analisis informacion publica congreso Chile


# Instalar (Dev)
```{python}
git clone https://github.com/felipenunezb/congreso_chile
pip install -e .
```

# Ejemplos
## Descargar informacion de votaciones y detalle por diputado en 2022
```
from congreso_chile.extract import getVotacionesDiputados
voto, diputado = getVotacionesDiputados(2022)
```

## Descargar informacion de votaciones y detalle por diputado en 2022, guardar json en directorio actual
```
from congreso_chile.extract import getVotacionesDiputados
voto, diputado = getVotacionesDiputados(2022, '.')
```

## Descargar informacion de votaciones y detalle por diputado en 2021 y 2022, guardar json en directorio actual
```
from congreso_chile.extract import getVotacionesDiputados
voto, diputado = getVotacionesDiputados([2021, 2022], '.')
```