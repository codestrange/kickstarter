import json
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

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
## ¿Qué es Kickstarter?

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
totales requeridos o las dificultades técnicas a ser superadas.
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
    #             "Nombre": item.name,
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
    #             "Nombre": item.name,
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

"""
**Categorías más exitosas**:
"""

# data = pd.DataFrame(
#     [
#         {
#             "name": item.name,
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
#             "name_total": cat.name,
#             "name_success": cat.name + " Exitosos",
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
    xaxis_rangeslider_visible=True,
)
timeline

"""
Teniendo en cuenta la información anterior se puede notar que muchas de las
categorías anteriores tuvieron un auge en Kickstarter durante los años del
2009 al 2014, pero desde entonces ya casi no aparecen proyectos a partir de
ese año. Un detalle interesante a tener en cuenta es que sobre esas fecha
aparece Patreon como un competidor de Kickstarter en el mercado, lo que podría
conllevar a que muchos proyectos se muden hacia esta nueva plataforma. Pero con
la categoría de juegos de mesa sucede algo interesante, y es que a partir de
esta fecha los proyectos de esa categoría han ido en aumento, tanto el total de
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
fig

"""
El dinero recaudado por los proyectos de Juegos de Mesa en Kickstarter
ha ido aumentando en el tiempo sostenidamente, llegando a alcanzar cifras
astronómicas como 200 millones de dólares. Notar los ligeros descensos en
el 2014 y 2020, que a priori se pueden justificar con apariciones de
plataformas alternativas y de la pandemia de la Covid-19 respectivamente.
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
fig

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
fig

"""
**Cantidad de proyectos exitosos de Juegos de Mesa segmentados por el dinero
recaudado y por año**
"""

# data = pd.DataFrame(
#     [
#         {
#             "date": date.year,
#             "value": value,
#             "label": label,
#         }
#         for date, value, label in zip(
#             *tabletop_games_model.successful_segmented_by_year()
#         )
#     ]
# )
# save_data("tabletop_games_4", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_4"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(name=label, x=data.date, y=item)  # type: ignore
        for item, label in zip(data.value, data.label)
    ],
    layout=go.Layout(barmode="stack"),  # type: ignore
)
fig

"""
**Dinero recaudado de los proyectos exitosos de Juegos de Mesa segmentados
por el dinero recaudado y por año**
"""

# data = pd.DataFrame(
#     [
#         {
#             "date": date.year,
#             "value": value,
#             "label": label,
#         }
#         for date, value, label in zip(
#             *tabletop_games_model.pledged_segmented_by_year(),
#         )
#     ]
# )
# save_data("tabletop_games_5", data.to_dict())
data = pd.DataFrame.from_dict(load_data("tabletop_games_5"))

fig = go.Figure(  # type: ignore
    data=[
        go.Bar(name=label, x=data.date, y=item)  # type: ignore
        for item, label in zip(data.value, data.label)
    ],
    layout=go.Layout(barmode="stack"),  # type: ignore
)
fig

"""
Examinar los proyectos por nivel de financiación es probablemente el mejor
indicador para entender el entorno de Kickstarter. Se puede observar como la
cantidad de proyectos por cada nivel de financiación han ido creciendo
equitativamente, manteniendo una homogeneidad en ese sentido.
"""
