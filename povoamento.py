import re
import json

with open("json/autores.json", "r", encoding="utf-8") as f:
    autores = json.load(f)

with open("json/editoras.json", "r", encoding="utf-8") as f:
    editoras = json.load(f)

with open("json/jogos.json", "r", encoding="utf-8") as f:
    jogos = json.load(f)

with open("json/mecanicas.json", "r", encoding="utf-8") as f:
    mecanicas = json.load(f)

with open("json/premios.json", "r", encoding="utf-8") as f:
    premios = json.load(f)

with open ("boardgames_base.ttl", "r", encoding="utf-8") as f:
    ontology_base = f.read()

autoresList = ""
editorasList = ""
jogosList = ""
mecanicasList = ""
premiosList = ""
categoriasList = ""
countriesList = ""
categoriesSet = set()
countriesSet = set()

for a in autores:
    autoresList += f"""
    :{a["id"].replace("-", "_")} a :Autor ;
             :id "{a["id"]}" ;
             :nome "{a["name"]}" ;
             :criou {', '.join(map(lambda j: f':{j.replace("-", "_")}', a["designedGames"]))} .
    """

for e in editoras:
    countriesSet.add(e["country"])

    editorasList += f"""
    :{e["id"].replace("-", "_")} a :Editora ;
             :id "{e["id"]}" ;
             :nome "{e["name"]}" ;
             :temPais "{e["country"]}" ;
             :publicou {', '.join(map(lambda j: f':{j.replace("-", "_")}', e["publishedGames"]))} .
    """

for j in jogos:
    categoriesSet.add(j["category"])

    jogosList += f"""
    :{j["id"].replace("-", "_")} a :Jogo ;
             :id "{j["id"]}" ;
             :nome "{j["name"]}" ;
             :duracao "{j["playingTimeMinutes"]}" ;
             :minJogadores "{j["minPlayers"]}" ;
             :maxJogadores "{j["maxPlayers"]}" ;
             :temCategoria :{j["category"]} ;
             :descricao "{j["descriptionEN"]}" .
    """

for m in mecanicas:
    mecanicasList += f"""
    :{m["id"].replace("-", "_")} a :Mecanica ;
             :id "{m["id"]}" ;
             :nome "{m["name"]}" ;
             :mecanicaDe {', '.join(map(lambda j: f':{j.replace("-", "_")}', m["usedInGames"]))} .
    """

for p in premios:
    premiosList += f"""
    :{p["id"].replace("-", "_")} a :Premio ;
             :id "{p["id"]}" ;
             :nome "{p["name"]}" ;
             :premiou :{p["wonByGame"].replace("-", "_")} .
    """

for c in categoriesSet:
    categoriasList += f"""
    :{c} a :Categoria ;
         :nome "{c}" .
    """

for country in countriesSet:
    countriesList += f"""
    :{country} a :Pais ;
         :nome "{country}" .
    """

genOntology = ontology_base + autoresList + editorasList + jogosList + mecanicasList + premiosList + categoriasList

with open("boardgames.ttl", "w", encoding="utf-8") as f:
    f.write(genOntology)
