# Search Engine em Python

Projeto acadêmico para busca e ranqueamento de documentos 

## Pré requisitos

  * Instalação de qualquer versão superior de Python 3 (http://www.python.org/download)
  
## Instalação das dependências

```bash
$ pip install -r requirements.txt
```

## Utilização

### primeiramente configure os arquivos main.cfg e gli.cfg
	- main.cfg -> informe quais módulos deseja rodar
	- gli.cfg -> informe o caminho dos arquivos a serem importados

```bash
>>> #executa a aplicação
>>> python search_engine.py 
>>> #avalia através de métricas em gráfico os resultados.
>>> python evaluating_the_results.py 
>>>
```