import json
from datetime import datetime

import pandas as pd

# import plotly
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

# from tabulate import tabulate

# from kickstarter.core import get_favorite_categories, load_json


def load_data(name: str):
    with open(f"jsons/{name}.json", mode="r", encoding="utf-8") as file:
        return json.load(file)


def save_data(name: str, data):
    with open(f"jsons/{name}.json", mode="w+", encoding="utf-8") as file:
        json.dump(data, file)


# projects, categories = load_json()
# favorite_categories = get_favorite_categories(projects, categories)

# grossing_gategories_model = favorite_categories[0]
# successful_categories_model = favorite_categories[1]
# grossing_categories = favorite_categories[2]
# successful_categories = favorite_categories[3]
# inter = favorite_categories[4]
# monthly_categories_success_model = favorite_categories[5]
# monthly_categories_totals_model = favorite_categories[6]
# by_months = favorite_categories[7]
# tabletop_games_model = favorite_categories[8]

st.set_page_config(
    page_title="Kickstarter y el Misterio de los Juegos de Mesa",
)

image = Image.open("images/header.jpg")
st.image(image, use_column_width=True)

"""
> _Por: Carlos Bermudez Porto, Leynier Gutiérrez González y Tony Raúl Blanco Fernández_
"""

"""
## ¿Qué es [Kickstarter](https://www.kickstarter.com)?

Kickstarter es un sitio web de micromecenazgo para proyectos creativos.​ Mediante
Kickstarter se ha financiado una amplia gama de proyectos, que van desde películas
independientes, música y cómics a periodismo, videojuegos y proyectos relacionados
con la comida.

Siendo uno nuevo en el conjunto de plataformas de recaudación de fondos llamado
"financiación en masa", Kickstarter facilita la captación de recursos monetarios
del público en general, un modelo que evita muchas vías tradicionales de
inversión. Los proyectos deben cumplir con las directrices de Kickstarter para
ponerse en marcha - proyectos de caridad, de causas, de "financiación de vida"
y recaudación de fondos sin límites fijos no están permitidos. Los dueños del
proyecto eligen una fecha límite y un mínimo objetivo de fondos a recaudar.
Si el objetivo elegido no es recolectado en el plazo, no se perciben fondos
(esto se conoce como provisión point mechanism). El dinero prometido por los
donantes se recopila mediante Amazon Payments.

Kickstarter toma un 5% de los fondos recaudados; Amazon cobra un 3–5% adicional.
A diferencia de muchos foros de recaudación de fondos o inversión, Kickstarter
renuncia a la propiedad sobre los proyectos y el trabajo que producen. Sin
embargo, los proyectos iniciados en el sitio son permanentemente archivados y
accesibles al público. Después de que la financiación se ha completado, los
proyectos y elementos multimedia subidos no pueden ser editados o eliminados
del sitio.

No hay garantía de que las personas que publican los proyectos en Kickstarter
cumplan sus proyectos, usen el dinero para poner en práctica sus proyectos o
que los proyectos concluidos satisfagan las expectativas de los patrocinadores,
y Kickstarter en sí ha sido acusado de proporcionar poco control de calidad.
Kickstarter aconseja a los patrocinadores que usen su propio juicio al apoyar
un proyecto. También advierten a los líderes de proyectos que podrían ser
responsables por los daños y perjuicios de los patrocinadores por no cumplir
las promesas. Los proyectos también pueden fallar, incluso después de una
recaudación de fondos exitosa, cuando los creadores subestiman los costos
totales requeridos o las dificultades técnicas a ser
superadas. [[1]](https://es.wikipedia.org/wiki/Kickstarter)
"""

"""
## ¿Cuáles son las categorías más exitosas?

Para crear un proyecto es necesario asignarle un categoría, estas son muy
variadas y brindan una importante información sobre el proyecto, ya que los
comportamientos de estos, el dinero necesario, etc dependerá mucho de qué tipo
(categoría) de proyecto se desee hacer.

Haciendo un análisis de las 25 categorías que más dinero han recaudado y de las
25 categorías con los porcentajes más altos de éxitos se deduce que las
categorías que aparecen en ambas listas sobresalen como categorías de interés
para los patrocinadores, y con mayores probabilidades de alcanzar sus metas, son:
"""

col_left, col_right = st.beta_columns(2)

with col_left:
    """
    **Top 25 - Más dinero recaudado**
    """
    # data = pd.DataFrame(
    #     [
    #         {
    #             "Nombre": item.translation,
    #             "$ Recaudados": grossing_gategories_model.counter[item.id],
    #         }
    #         for item in grossing_categories
    #     ]
    # )
    # save_data("top25pledged", data.to_dict())
    data = pd.DataFrame.from_dict(load_data("top25pledged"))
    st.write(data)

with col_right:
    """
    **Top 25 - Mejor porcentaje de éxitos**
    """
    # data = pd.DataFrame(
    #     [
    #         {
    #             "Nombre": item.translation,
    #             "% Éxitos": str(
    #                 round(
    #                     successful_categories_model.categories_success[item.id]
    #                     / successful_categories_model.categories_total[item.id]
    #                     * 100,
    #                     2,
    #                 )
    #             )
    #             + "%",
    #         }
    #         for item in successful_categories
    #     ]
    # )
    # save_data("top25successful", data.to_dict())
    data = pd.DataFrame.from_dict(load_data("top25successful"))
    st.write(data)
    # st.write(tabulate(data, tablefmt="html"))

"""
**Categorías más exitosas**:
"""

# data = pd.DataFrame(
#     [
#         {
#             "name": item.translation,
#             "pledged": grossing_gategories_model.counter[item.id],
#             "success": round(
#                 successful_categories_model.categories_success[item.id]
#                 / successful_categories_model.categories_total[item.id]
#                 * 100,
#                 2,
#             ),
#         }
#         for item in inter
#     ]
# )
# save_data("topcategories", data.to_dict())
data = pd.DataFrame.from_dict(load_data("topcategories"))

for item in data.itertuples():
    f"""
    * {item.name}:
        * Dinero Recaudado: ${item.pledged}
        * Porcentaje de Éxitos: {item.success}%
    """

"""
## ¿Cómo se han comportado estas categorías a lo largo del tiempo?

Si bien en general las categorías antes mencionadas aparecen como las más
prometedoras, este éxito podría verse enmarcado en un determinado momento
y no como algo sostenido en el tiempo. Por eso es necesario analizar el
comportamiento de estas en los últimos años.

En las siguientes gráficas mostramos la cantidad de proyectos por categorías,
así como la cantidad de estos que fueron exitosos, por mes durante los años
del 2009 al 2020.
"""

timeline = go.Figure()  # type: ignore

# data = pd.DataFrame(
#     [
#         {
#             "name_total": cat.translation,
#             "name_success": cat.translation + " Exitosos",
#             "x_total": [
#                 (
#                     monthly_categories_totals_model.dates[i].year,
#                     monthly_categories_totals_model.dates[i].month,
#                 )
#                 for i in range(len(monthly_categories_success_model.dates))
#             ],
#             "y_total": [
#                 monthly_categories_totals_model.categories[cat.id][i]
#                 for i in range(len(monthly_categories_success_model.dates))
#             ],
#             "x_success": [
#                 (
#                     monthly_categories_success_model.dates[i].year,
#                     monthly_categories_success_model.dates[i].month,
#                 )
#                 for i in range(len(monthly_categories_success_model.dates))
#             ],
#             "y_success": [
#                 monthly_categories_success_model.categories[cat.id][i]
#                 for i in range(len(monthly_categories_success_model.dates))
#             ],
#         }
#         for cat in inter
#     ]
# )
# save_data("timeline", data.to_dict())
data = pd.DataFrame.from_dict(load_data("timeline"))

for item in data.itertuples():
    timeline.add_scatter(
        x=[datetime(year=y, month=m, day=1) for y, m in item.x_total],
        y=item.y_total,
        name=item.name_total,
        opacity=0.9,
    )
    timeline.add_scatter(
        x=[datetime(year=y, month=m, day=1) for y, m in item.x_success],
        y=item.y_success,
        name=item.name_success,
        opacity=0.9,
    )

timeline.update_layout(
    title_text="Cantidad de Proyectos vs Cantidad de Proyectos Exitosos",
    xaxis_title="Fecha",
    yaxis_title="Cantidad",
    xaxis_rangeslider_visible=True,
)
timeline
# plotly.offline.plot(timeline, filename="timeline.html")  # type: ignore

"""
Teniendo en cuenta la información anterior se puede notar que muchas de las
categorías anteriores tuvieron un auge en Kickstarter durante los años del
2009 al 2014, pero desde entonces ya casi no aparecen proyectos a partir de
ese año. Un detalle interesante a tener en cuenta es que sobre esas fecha
aparece [Patreon](https://www.patreon.com/) como un competidor de Kickstarter
en el mercado, lo que podría conllevar a que muchos proyectos se muden hacia
esta nueva plataforma.
"""

"""
### Cómics en Patreon
"""

image = Image.open("images/comics_1_patreon.jpg")
st.image(image, use_column_width=True)

image = Image.open("images/comics_2_patreon.jpg")
st.image(image, use_column_width=True)

"""
> Tomado de [graphtreon.com](https://graphtreon.com)

Se puede observar como en la plataforma de Patreon el dinero recaudado y la
cantidad de creadores ha ido en aumento desde el 2016.
"""

"""
### Cortometrajes en Patreon

Si bien no hay una categoría en Patreon de Cortometrajes exactamente, es posible
tomar una idea juntando las categorías de Animación y Video.
"""

col_left, col_right = st.beta_columns(2)

with col_left:
    image = Image.open("images/shorts_1_patreon.jpg")
    st.image(image, use_column_width=True)
    image = Image.open("images/shorts_2_patreon.jpg")
    st.image(image, use_column_width=True)

with col_right:
    image = Image.open("images/shorts_3_patreon.jpg")
    st.image(image, use_column_width=True)
    image = Image.open("images/shorts_4_patreon.jpg")
    st.image(image, use_column_width=True)

"""
> Tomado de [graphtreon.com](https://graphtreon.com)

Al igual que los cómics en Patreon se puede observar cómo el dinero recaudado
y la cantidad de creadores ha ido en aumento desde el 2016 en ambas categorías
(animación y video).
"""

"""
----------------------------------------------------------------------------

Pero con la categoría de juegos de mesa sucede algo interesante, y es que a partir
de esta fecha los proyectos de esa categoría han ido en aumento, tanto el total de
proyectos en la categoría como el porcentaje de éxito de las campañas.
"""

"""
## Estadísticas sobre los Juegos de Mesa
"""

"""
**Dinero recaudado por año de los proyectos exitosos de Juegos de Mesa**
"""

# data = pd.DataFrame(
#     [
#         {
#             "date": date.year,
#             "value": value,
#         }
#         for date, value in zip(*tabletop_games_model.pleged_by_year())
#     ]
# )
# save_data("tabletop_games_1", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_1"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(x=data.date, y=data.value),  # type: ignore
    ],
    layout=go.Layout(barmode="overlay"),  # type: ignore
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="USD Recaudados en millones",
)

fig
# plotly.offline.plot(fig, filename="tabletop_games_1.html")  # type: ignore

"""
El dinero recaudado por los proyectos de Juegos de Mesa en Kickstarter ha ido
aumentando en el tiempo sostenidamente, llegando a alcanzar cifras astronómicas
como 200 millones de dólares. Notar los ligeros descensos en el 2014 y 2020. En
el caso del año 2014 la web de Kickstarter sufrió varios  cambios a lo largo del
año. Al ser esta la única fuente posible de extracción  de datos de los proyectos,
estos cambios hicieron que muchos de los motores  que los recogen sufrieran
problemas para realizar su tarea. Por tanto se  pudiera explicar esta ligera
diferencia en cuanto a la recaudación de los  proyectos en ese año. Está también
el hecho de que ese año fue considerado un  buen año para la plataforma
[Indiegogo](https://www.indiegogo.com),
la cual es un rival de Kickstarter  en el sector. Para el 2020, a pesar de aun no
estar finalizado el año, se  puede ver que la pandemia de Covid-19 tuvo su impacto
en este sector. Esto  producto de la crisis económica que afectó a las personas y
sus posibles  donaciones.
"""

"""
**Exitosos vs Total por año de los proyectos de Juegos de Mesa**
"""

# data = pd.DataFrame(
#     [
#         {
#             "date": date.year,
#             "successful": successful,
#             "total": total,
#         }
#         for date, successful, total in zip(
#             *tabletop_games_model.successful_vs_total_by_year()
#         )
#     ]
# )
# save_data("tabletop_games_2", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_2"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(name="Total", x=data.date, y=data.total),  # type: ignore
        go.Bar(name="Exitosos", x=data.date, y=data.successful),  # type: ignore
    ],
    layout=go.Layout(barmode="overlay"),  # type: ignore
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Cantidad",
)

fig
# plotly.offline.plot(fig, filename="tabletop_games_2.html")  # type: ignore

"""
Como es lógico a la par del aumento del dinero recaudado por los proyectos
de Juegos de Mesa también ha ido en aumento la cantidad de proyectos de este
tipo en la plataforma. Interesante observar que los porcentajes de proyectos
exitosos también han ido en aumento (todo lo anterior con las excepciones de
2015 y 2020). Pero más interesante aún es que la velocidad del aumento de los
proyectos exitosos está siendo mayor que la del total de proyectos de la
categoría, como se puede observar en la siguiente gráfica.
"""

# data = pd.DataFrame(
#     [
#         {
#             "date": date.year,
#             "value": value,
#         }
#         for date, value in zip(
#             *tabletop_games_model.successful_vs_total_percent_by_year()
#         )
#     ]
# )
# save_data("tabletop_games_3", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_3"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(x=data.date, y=data.value),  # type: ignore
    ],
    layout=go.Layout(barmode="overlay"),  # type: ignore
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Porciento de Exito",
)

fig
# plotly.offline.plot(fig, filename="tabletop_games_3.html")  # type: ignore

"""
**Cantidad de proyectos exitosos de Juegos de Mesa segmentados por el dinero
recaudado y por año**
"""

# dates, values, labels = tabletop_games_model.successful_segmented_by_year()
# data = pd.DataFrame(
#     [
#         {
#             "date": [date.year for date in dates],
#             "value": value,
#             "label": label,
#         }
#         for value, label in zip(values, labels)
#     ]
# )
# save_data("tabletop_games_4", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_4"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(name=label, x=date, y=item)  # type: ignore
        for date, item, label in zip(data.date, data.value, data.label)
    ],
    layout=go.Layout(barmode="stack"),  # type: ignore
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Cantidad de Proyectos",
)

fig
# plotly.offline.plot(fig, filename="tabletop_games_4.html")  # type: ignore

"""
**Dinero recaudado de los proyectos exitosos de Juegos de Mesa segmentados
por el dinero recaudado y por año**
"""

# dates, values, labels = tabletop_games_model.pledged_segmented_by_year()
# data = pd.DataFrame(
#     [
#         {
#             "date": [date.year for date in dates],
#             "value": value,
#             "label": label,
#         }
#         for value, label in zip(values, labels)
#     ]
# )
# save_data("tabletop_games_5", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_5"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(name=label, x=date, y=item)  # type: ignore
        for date, item, label in zip(data.date, data.value, data.label)
    ],
    layout=go.Layout(barmode="stack"),  # type: ignore
)

fig.update_layout(
    xaxis_title="Año",
    yaxis_title="USD Recaudados en Millones",
)

fig
# plotly.offline.plot(fig, filename="tabletop_games_5.html")  # type: ignore

"""
> Idea de análisis tomada
de: [icopartners.com](https://icopartners.com/2020/01/kickstarter-and-games-in-2019)

Examinar los proyectos por nivel de financiación es probablemente el mejor
indicador para entender el entorno de Kickstarter. Se puede observar como la
cantidad de proyectos por cada nivel de financiación han ido creciendo
equitativamente, manteniendo una homogeneidad en ese sentido.
"""

"""
## ¿Qué juegos de mesa han recaudado más?

Los diez juegos de mesa que han recaudado más dinero a lo largo del tiempo han sido
los siguientes:
"""

# top_ten_all_the_time_projects = tabletop_games_model.top_ten_all_the_time_games()
# data = pd.DataFrame(
#     [
#         {
#             "Nombre": project.name,
#             "Recaudación": project.pledged,
#         }
#         for project in top_ten_all_the_time_projects
#     ]
# )
# save_data("top_ten_all_the_time_projects", data.to_dict())
data = pd.DataFrame.from_dict(load_data("top_ten_all_the_time_projects"))

data
# "top_ten_all_the_time_projects"
# st.write(tabulate(data, tablefmt="html"))

"""
Interesante como los dos que más han recaudado se separan bastante del
resto representando el `31.16%` del dinero total recaudado del top 10.
"""

"""
Los diez juegos de mesa que han recaudado más en el transcurso del 2020:
"""

# top_ten_2020_games = tabletop_games_model.top_ten_2020_games()
# data = pd.DataFrame(
#     [
#         {
#             "Nombre": project.name,
#             "Recaudación": project.pledged,
#         }
#         for project in top_ten_2020_games
#     ]
# )
# save_data("top_ten_2020_games", data.to_dict())
data = pd.DataFrame.from_dict(load_data("top_ten_2020_games"))

data
# "top_ten_2020_games"
# st.write(tabulate(data, tablefmt="html"))

"""
El 2020 está siendo un año con juegos con muy buena recaudación, teniendo 7 juegos
en común con el top 10 de todos los tiempos, destacándose **Frosthaven** como el
juego de mesa con más recaudación de todos los tiempos.
"""

# inter_set = set(top_ten_all_the_time_projects).intersection(set(top_ten_2020_games))

# inter_list = list(inter_set)
# inter_list.sort(key=lambda x: x.pledged, reverse=True)

# data = pd.DataFrame(
#     [
#         {
#             "Nombre": project.name,
#             "Recaudación": project.pledged,
#         }
#         for project in inter_list
#     ]
# )
# save_data("inter_list", data.to_dict())
data = pd.DataFrame.from_dict(load_data("inter_list"))

data
# "inter_list"
# st.write(tabulate(data, tablefmt="html"))

"""
## ¿Por qué el auge de los Juegos de Mesa en Kickstarter?

Uno de los motivos más claros es que Kickstarter ofrece la oportunidad de
que las ideas de empresas pequeñas y diseñadores individuales de juegos se
materialicen. Antes de la creación de Kickstarter, las ideas de los
diseñadores de juegos de mesa eran presentadas a los editores de grandes
compañías y esperar a que fueran elegidas para financiamiento y publicación,
o por lo contrario, el financiamiento tendría que correr por el diseñador lo
cual impedía grandemente la creación de los juegos de mesa.

Otro factor a tener en cuenta es la competencia, al disminuir el nivel de
entrada en la industria de juegos de mesa, ha provocado un crecimiento de la
calidad de estos. A medida que los diseñadores de juegos compiten por hacerse
notar en la inmensa cantidad de proyectos, los impulsa a explorar nuevas
mecánicas de juego creativas. El desarrollo de la impresión 3D ha provocado
un auge en el uso de miniaturas elaboradas, los niveles de compromiso han
llevado a una mayor variedad de materiales de calidad como madera o metal, y
un enfoque cada vez mayor en la apariencia estética de los juegos se ha
derivado de la necesidad de captar la atención de posibles patrocinadores.
Como usuario consumidor, esto da como resultado una variedad más amplia de
géneros, juegos más atractivos, reglas y conceptos más creativos.

El feedback es otro factor importante, Kickstarter no sólo ofrece una
plataforma en la que se financian productos, sino también un sentido de
comunidad entre el creador y los patrocinadores del proyecto. Esto permite
que tanto los diseñadores de juegos como los usuarios interactúen entre sí a
través de la sección de comentarios, dando a los usuarios una valoración del
producto y a los diseñadores una idea de la aceptación del producto. La
comunidad se convierte en parte de una narrativa en la que ellos y los
desarrolladores luchan juntos contra el tiempo para alcanzar la fecha límite
de financiación y los ambiciosos
objetivos. [[2]
](https://www.boardgameatlas.com/forum/Xy8J2tXge2/how-kickstarter-has-changed-board-games-)
"""

"""
## Posibles amenazas al sector de Juegos de Mesa y Kickstarter

Las influencias externas complicaron el objetivo de Kickstarter a lo largo de
2019. La principal de ellas es el esfuerzo continuo de sindicalización dentro
de la empresa . Tanto la gerencia de Kickstarter como el incipiente Kickstarter
United han acordado un apagón de los medios hasta que se resuelva el
problema. [[3]
](https://www.polygon.com/2019/9/16/20868406/kickstarter-union-firings-dispute-petition)

El 18 de febrero de 2020 los empleados de Kickstarter votaron para formar un
sindicato, convirtiéndose en la primera gran empresa de tecnología de los Estados
Unidos en hacerlo. [[4]](https://kickstarterunited.org)

Aún más amenazante es la guerra comercial en curso entre Estados Unidos y
China. Muchos juegos de mesa se fabrican en China, y los esfuerzos de la
administración del expresidente Trump de los Estados Unidos por ejercer presión
han creado malestar entre los creadores de juegos de
mesa. [[5]](https://www.polygon.com/2019/6/5/18652411/trump-china-tariff-board-games)
"""

"""
## Metodología

Los análisis anteriores fueron realizados a partir de los datos obtenidos
y publicados por la página
[webrobots.io/kickstarter-datasets](https://webrobots.io/kickstarter-datasets/).
Los datos de los proyectos se encuentran en varios paquetes, obtenidos
de scrappear el sitio de Kickstarter los días 15 de cada mes desde el
año 2015 hasta noviembre del 2020. Debido a que los proyectos varían en
el tiempo muchos se encuentran enmarcados en diferentes paquetes de los
mencionados. Para evitar repeticiones fue necesario realizar un
preprocesamiento de los datos de los proyectos, a la vez que se realizaba
un filtrado de algunas de sus propiedades. Con los datos resultantes es
que se realizaron los diferentes estudios mostrados en este artículo.

Los códigos que realizan ambos procesamientos de los datos son
accesibles desde nuestro
[repositorio](https://github.com/codestrange/kickstarter/tree/main/kickstarter)
en Github.
"""

"""
## Referencias

1. [Kickstarter Wikipedia](https://es.wikipedia.org/wiki/Kickstarter)
2. [How Kickstarter has CHANGED Board Games
](https://www.boardgameatlas.com/forum/Xy8J2tXge2/how-kickstarter-has-changed-board-games-)
3. [Kickstarter under fire from creators over labor dispute
](https://www.polygon.com/2019/9/16/20868406/kickstarter-union-firings-dispute-petition)
4. [Kickstarter United](https://kickstarterunited.org)
5. [Trump’s tariffs could ruin the American board gameindustry
](https://www.polygon.com/2019/6/5/18652411/trump-china-tariff-board-games)
"""
