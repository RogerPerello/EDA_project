# EDA - La guerra de Ucrania: precios, bajas y refugiados

<p align="center">
    <img src="/src/data/foto_eda.png" width="1000">
</p>

Este EDA (del inglés, análisis exploratorio de datos) es un ejercicio para el programa Part Time de la plataforma THEBRIDGE. Se utilizan tablas con datos de distintas fuentes originales, relacionadas con la guerra de Ucrania, y se les asignan una serie de hipótesis. Durante el transcurso de las pesquisas, las hay que se prueban y que se desmienten, y se encuentran, por añadidura, otros datos relevantes que sirven como conclusiones.

Se tiene en cuenta que los datos pueden estar sesgados, ya que en general proceden de fuentes ucranianas, aunque la coherencia entre las distintas tablas y el hecho de que vayan acompañadas, en algunos casos, de fotografías, así como la reputación de la plataforma de la que provienen la mayoría —es decir, Kaggle—, los dotan de congruencia. Esas imágenes pueden descargarse de la propia web, en la página del dataset correspondiente.

Para las pruebas que dan como resultado un pvalor (como el ttest), como se trata de un ejercicio, se trabaja como si las distribuciones fueran de tipo normal. A las conclusiones de cada hipótesis las siguen teorías que explican en qué puede traducirse tal o cual argumento matemático si se le busca una significación. Convergen, por esta vía, los datos “puros”, calculados directamente de las tablas obtenidas, y la reflexión posterior.

En base a esos razonamientos, las conclusiones finales van un punto más allá: con una combinación de los desenlaces de cada hipótesis, se le proponen al bando ucraniano una serie de consideraciones. Por ejemplo, como en la hipótesis 1 se detecta que el precio de los medicamentos importados no cambia en función de la cercanía al frente de las ciudades, se comenta que no sería necesario aplicar una rebaja a las que están más próximas a la batalla. Asimismo, como el precio de algunos oscila y crece con el paso de la guerra, se recomienda solicitar a los aliados que los envíen con más frecuencia. 

El valor de esos juicios últimos deberá sopesarlo el lector con los datos en mano y haciendo uso de su sentido común, pues no dejan de ser apreciaciones que, si bien están muy pensadas, no están exentas —como es inevitable para este tipo de deducciones— de un cierto grado de subjetividad. Tanto si se estiman ciertas como si no, habrán cumplido su propósito con creces si sirven como método de aprendizaje, para animar el debate o para promover algún que otro análisis que las desmienta o corrobore.


## Guía de carpetas
### [Diapositivas](/Diapositivas.pptx)
- Proyecciones en Power Point empleadas la presentación del trabajo.
### [Memoria](/Memoria.pdf)
- Documento que detalla el proceso (con limpieza, hipótesis y total de conclusiones).
- Incluye anexos con los gráficos, así como otras imágenes aclaratorias.
### [Referencias](/Referencias.pdf)
- Listado de páginas utilizadas a modo de apoyo durante el proyecto.
- Se dividen por su enfoque, que puede ser formal o de contenidos.
### [src](/src)
- [EDA](/src/EDA.pdf), que es la versión final del código en un Jupiter de Python.
- [data](/src/data), que contiene imágenes importadas por algunos archivos y los datasets originales.
- [notebooks](/src/notebooks), con todas las pruebas repartidas por diversos notebooks Jupiter.
- [utils](/src/utils), con aquellas funciones de uso frecuente que se llaman en el archivo EDA.


## Punto de partida
Se parte de seis datasets de tamaños variables sobre diversos aspectos de la guerra de Ucrania que tienen que ver con las pérdidas (sobre todo, las rusas, de las que hay más datos disponibles), los refugiados y los precios en los mercados locales. El nexo de la mayoría son las fechas. Las hipótesis son:
1) Los precios en Ucrania oscilan en función del número de refugiados huidos del país (cuantos más hay, menos demanda) y de la cercanía al frente de los puestos de venta (cuanto más cerca están, más costoso es transportar los productos, y más caros se venden). Asimismo, un peor rendimiento del bando ruso debe animar a los proveedores extranjeros a vender en el país y aumentar la oferta (con lo cual los productos son más baratos).
A modo de esquema, se puede resumir así:
[Más refugiados, mayor lejanía del frente o más pérdidas rusas = precios más bajos]

2) Con el paso del tiempo, aumentan las pérdidas materiales rusas y se reducen las humanas. Ello es indicativo de una creciente preocupación de la administración rusa por la opinión pública, con lo que, entre otras cosas, se sirve menos de infantería para minimizar la cuenta de bajas.
A modo de esquema, se puede resumir así:
[Uso mayor de tropas mecanizadas = uso reducido de soldados rasos = más pérdidas materiales y menos muertos]

3) Los ejércitos ruso y ucraniano utilizan mucho material de la Unión Soviética, que, en comparación con el equipamiento moderno, tiende a fallar y a capturarse con mayor frecuencia.
A modo de esquema, se puede resumir así:
[Uso de material soviético = más capturas]

## Algunas conclusiones
-	No hay relación entre la cercanía al frente y el precio de los productos. La guerra moderna, con artillería de larga distancia y bombardeos aéreos, y con un frente amplio, implica que todas las ciudades sean susceptibles de sufrir problemas puntuales de suministro independientemente de su proximidad al enemigo.
<img src="/src/data/1-product_by_distance.png" width="400">


-	Los precios de los antibióticos y los antipiréticos, además de ser superiores en términos generales, oscilan mucho. Como el país se encuentra en situación de guerra, es de prever que la demanda de este tipo de medicamentos, muy útiles para una persona herida o con fiebre, se haya elevado. De ahí que oscilen y se encarezcan de un modo dramático comparados con los agentes vasodilatadores, que sirven para tratar la tensión arterial, un problema de salud cuyos factores de riesgo no se ven agravados en un conflicto bélico.
<img src="/src/data/2-med_by_distance.png" width="400">


-	Es poco probable que las diferencias en el precio de los medicamentos de ciudad a ciudad, por sí solas, supongan un problema para los consumidores, ya que el índice de Gini es bajo para todas; el único problema sería que la demanda subiese tanto que llegasen a escasear (o que la oferta se redujese).
<img src="/src/data/3-med_gini.png" width="400">


-	La mayoría de bajas son de APC. Esas son las siglas de Armored Personnel Carrier, lo cual implica que hay bajas de personal simultáneamente, ya que se destruyen vehículos dedicados al transporte de personal, si bien con capacidades defensivas.
<img src="/src/data/4-losses_by_type.png" width="400">


- La mayor parte de bajas diarias para el período del sexto al noveno mes están por debajo de la mediana.
<img src="/src/data/5-losses_by_date.png" width="400">


-	La mayoría de pérdidas del bando ruso son vehículos de transporte de infantería armados (soviéticos) y vehículos de transporte no armados (no soviéticos).
<img src="/src/data/6-losses_soviet_or_not.png" width="400">
