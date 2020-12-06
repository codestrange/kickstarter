from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st
from PIL import Image

from kickstarter.core import get_favorite_categories as get_favorite_categories_raw
from kickstarter.core import load_json as load_json_raw
from kickstarter.models import CategoryModel, ProjectModel
from kickstarter.processing import GrossingCategoriesModel, SuccessfulCategoriesModel

image = Image.open("images/logo.png")
st.image(image, use_column_width=True)


def load_json() -> Tuple[
    List[ProjectModel],
    Dict[int, CategoryModel],
]:
    return load_json_raw()


def get_favorite_categories(
    projects: List[ProjectModel],
    categories: Dict[int, CategoryModel],
) -> Tuple[
    GrossingCategoriesModel,
    SuccessfulCategoriesModel,
    List[CategoryModel],
    List[CategoryModel],
    List[CategoryModel],
]:
    return get_favorite_categories_raw(projects, categories)


"""
# ¿Qué hace que un proyecto sea exitoso en [Kickstarter](https://www.kickstarter.com)?
"""

"""
> _Por: Carlos Bermudez Porto, Leynier Gutiérrez González y Tony Raúl Blanco Fernández_
"""

"""
### ¿Qué es [Kickstarter](https://www.kickstarter.com)?

**Kickstarter** es un sitio web de micromecenazgo para proyectos creativos.​ Mediante
**Kickstarter** se ha financiado una amplia gama de proyectos, que van desde películas
independientes, música y cómics a periodismo, videojuegos y proyectos relacionados con
la comida.

Siendo uno nuevo en el conjunto de plataformas de recaudación de fondos llamado
"financiación en masa", **Kickstarter** facilita la captación de recursos monetarios
del público en general, un modelo que evita muchas vías tradicionales de inversión.
Los proyectos deben cumplir con las directrices de **Kickstarter** para ponerse en
marcha - proyectos de caridad, de causas, de "financiación de vida" y recaudación de
fondos sin límites fijos no están permitidos. Los dueños del proyecto eligen una fecha
límite y un mínimo objetivo de fondos a recaudar. Si el objetivo elegido no es
recolectado en el plazo, no se perciben fondos (esto se conoce como provision point
mechanism). El dinero prometido por los donantes se recopila mediante Amazon Payments.

**Kickstarter** toma un 5% de los fondos recaudados; Amazon cobra un 3–5% adicional.
A diferencia de muchos foros de recaudación de fondos o inversión, **Kickstarter**
renuncia a la propiedad sobre los proyectos y el trabajo que producen. Sin embargo,
los proyectos iniciados en el sitio son permanentemente archivados y accesibles al
público. Después de que la financiación se ha completado, los proyectos y elementos
multimedia subidos no pueden ser editados o eliminados del sitio.

No hay garantía de que las personas que publican los proyectos en **Kickstarter**
cumplan sus proyectos, usen el dinero para poner en práctica sus proyectos o que los
proyectos concluidos satisfagan las expectativas de los patrocinadores, y
**Kickstarter** en sí ha sido acusado de proporcionar poco control de calidad.
**Kickstarter** aconseja a los patrocinadores que usen su propio juicio al apoyar
a un proyecto. También advierten a los líderes de proyectos que podrían ser
responsables por los daños y perjuicios de los patrocinadores por no cumplir las
promesas. Los proyectos también pueden fallar, incluso después de una recaudación
de fondos exitosa, cuando los creadores subestiman los costos totales requeridos o
las dificultades técnicas a ser superadas.
"""

"""
### ¿Cuáles son las categorías más exitosas?

Para crear un proyecto es necesario asignarle un categoría, estas son muy variadas
y brindan una importante información sobre el proyecto, ya que los comportamientos
de estos, el dinero necesario, etc dependerá mucho de que tipo (categoría) de proyecto
se desee hacer.

Haciendo un análisis de las 25 categorías que más dinero han recaudado y de las 25
categorías con los porcientos más altos de éxitos las categorías que aparecen en ambas
listas sobresaliendo como categorías de interes para los patrocinadores, y con mayores
probabilidades de alcanzar sus metas, son:
"""

favorite_categories: Tuple[
    GrossingCategoriesModel,
    SuccessfulCategoriesModel,
    List[CategoryModel],
    List[CategoryModel],
    List[CategoryModel],
] = get_favorite_categories(
    *load_json()  # type: ignore
)

col1, col2 = st.beta_columns(2)

with col1:
    data_frame = pd.DataFrame(
        [
            {
                "name": item.name,
                "pleged": favorite_categories[0].counter[item.id],
            }
            for item in favorite_categories[2]
        ]
    )
    st.write("Top 25 - Más dinero recaudado")
    st.write(data_frame)

with col2:
    data_frame = pd.DataFrame(
        [
            {
                "name": item.name,
                "success": favorite_categories[1].categories_success[item.id]
                / favorite_categories[1].categories_total[item.id],
            }
            for item in favorite_categories[3]
        ]
    )
    st.write("Top 25 - Mejor porciento de metas cumplidas")
    st.write(data_frame)

data_frame = pd.DataFrame(
    [
        {
            "name": item.name,
            "pleged": favorite_categories[0].counter[item.id],
            "success": favorite_categories[1].categories_success[item.id]
            / favorite_categories[1].categories_total[item.id],
        }
        for item in favorite_categories[4]
    ]
)

st.dataframe(data_frame)

"""
### ¿Cómo se han comportado estas categorías a lo largo del tiempo?

Si bien en general las categorías antes mencionadas aparecen como las más
prometedoras, este éxito podría verse enmarcado en un determinado momento y
no como algo que ocuerre casi todo el tiempo. Por eso es necesario analisar
el comportamiento de estas en los últimos años.

En las siguientes gráficas mostramos la cantidad de proyectos, asi como la
cantidad de estos que fueron exitosos, de estas categorías por mes durante
los años del 2009 al 2018.
"""

"""
Teniendo en cuenta la información anterior podemos notar que muchas de las
categorías anteriores tuvieron un auge en **Kickstarter** durante los años
del 2009 al 2014, pero desde entonces ya casi no aparecen proyectos a partir
de ese año. Un detalle interesante a tener en cuenta es que sobre esas fecha
aparece [**Patreon**](https://www.patreon.com) como un competidor de
**Kickstarter** en el mercado, lo que podría conllevar a que muchos proyectos
se muden hacia esta nueva plataforma. Solo mantienen un ritmo mas estable las
categorías de Libros para niños, No ficción, Película narrativa y Vídeojuegos.
"""

"""
### ¿Influirá la temporada del año en el éxito de un proyecto?

En principio una puede pensar que dependiendo de la temporada del año en que se
da a conocer un proyecto, este pueda lograr ser exitoso o no. Esto debido a muchas
rasones, por ejemplo, un festival de música no me interesa mucho si este se va a
realizar en tiempo de pruebas finales. Este tipo de situaciones son muy frecuentes
y pueden ser decisivas para un proyecto.

A continuación analizaremos como se comportan las categorías que han sido y son
más exitosas dependiendo del més del año en que sus proyectos fueron dados a conocer.
"""
