# Web Scraping

## Beautiful Soup

BeautifulSoup es una biblioteca de Python para extraer datos de documentos HTML y XML.

Para poder utilizarlo, primero debemos leer el archivo como texto y guardarlo en una variable. Luego hay que instanciar `BeautifulSoup` pasándole la página web y un *parser*; este último nos ayuda a identificar si el archivo viene en XML o HTML.

```python
from bs4 import BeautifulSoup

soup = BeautifoulSoup(webpage, parser='html.parser')
```

BeautifulSoup nos permite obtener elementos de una página web de una forma Pythonica, usando notación de objetos. Por ejemplo si queremos acceder al `title` de la página usamos `soup.title`. **Siempre nos dará la primer etiqueta que aparezca en el documento**. Algunos atributos de las etiquetas son:

* `soup.element.name`: Nos da el nombre de la etiqueta.
* `soup.element.string`: Nos da el texto que se encuentra dentro de la etiqueta

Si usamos `soup.prettify()` podemos imprimir el documento formateado de HTML.

### Obtener todas las etiquetas

Podemos obtener todas las etiquetas con la función `find_all()`. Esto nos devuelve un objeto de tipo `ResultSet` con todas las etiquetas encontradas.

```python
# Name debe ser el nombre de la etiqueta que estamos buscando
soup.find_all(
    name=tag_name,     # Busca todas las etiquetas del mismo nombre
    id=tag_id,         # Busca todas las etiquetas del mismo id
    class_=tag_class,  # Busca todas las etiquetas de la misma clase
    )
```

Luego podemos iterar por cada una de las etiquetas y obtener los textos. Por ejemplo:

```python
for tag in all_tags:
    print(tag.getText())
```

### Obtener atributos

Podemos obtener los atributos de nuestras etiquetas, por ejemplo, `href` de una etiqueta `<a> </a>`, usando la función `.get()`.

```python
tag.get("attribute")
```

### Usar selectores de CSS

Podemos obtener etiquetas usando selectores de CSS. Para esto debemos utilizar la función `soup.select_one()` para obtener un único elemento o `soup.select()` para obtener varios elementos.

```python
soup.select_one(selector='p a')  # Obtenemos todos los a dentro de p
soup.select_one(selector='#some_tag_id')  # Obtenemos todos los a dentro de p
soup.select(selector='.tag_class')  # Obtenemos todos los a dentro de p
```
