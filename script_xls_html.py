import pandas as pd
import os
import re

# Cargar el archivo XLS
df = pd.read_excel('LIBRERÍA_AGUAS_ABAJO.xlsx')

# Seleccionar las columnas necesarias y manejar NAN
df = df[['TÍTULO', 'AUTOR', 'AÑO', 'ISBN', 'EDITORIAL', 'PRECIO VENTA']].fillna({
    'ISBN': "No disponible",
    'AÑO': "No disponible"
})

# Crear una carpeta para las páginas
os.makedirs('catálogo', exist_ok=True)

# Generar las páginas HTML
for index, row in df.iterrows():
    title = row['TÍTULO'].replace(' ', '_')
    isbn_value = str(int(row['ISBN'])) if row['ISBN'] != "No disponible" else "No disponible"
    year_value = str(int(row['AÑO'])) if row['AÑO'] != "No disponible" else "No disponible"

    html_content = f"""
    <html>
    <head>
        <title>{row['TÍTULO']}</title>
        <style>
            body {{ font-family: Atkinson hyperlegible, sans-serif; text-align: center; margin: 20px; padding: 20px; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9; }}
            h1 {{ color: #333; }}
            .info {{ margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #fff; }}
            #modal {{ position: fixed; z-index: 1000; left: 0; top: 0; width: 60%; height: auto; overflow: auto; background-color: rgba(0, 0, 0, 0.8); display: none; }}
            #modal img {{ display: block; margin: auto; max-width: 80%; max-height: 80%; }}
        </style>
    </head>
    <body>
        <h1>{row['TÍTULO']}</h1>
        <div>
            <img id="{title}_cover" src="../img/{title}_cover.jpg" width="300" alt="Portada" style="cursor:pointer;">
            <img id="{title}_back" src="../img/{title}_back.jpg" width="300" alt="Contraportada" style="cursor:pointer;">
            <img id="{title}_in" src="../img/{title}_in.jpg" width="300" alt="Interior" style="cursor:pointer;">
        </div>
        <div id="modal">
            <span id="cerrar" style="cursor:pointer; color: white;">&times;</span>
            <img id="imgModal" src="" style="width:100%;">
        </div>
        <div class="info">
            <p><strong>Autor:</strong> {row['AUTOR']}</p>
            <p><strong>Año:</strong> {year_value}</p> 
            <p><strong>ISBN:</strong> {isbn_value}</
                        <p><strong>Editorial:</strong> {row['EDITORIAL']}</p>
            <p><strong>Precio:</strong> ${row['PRECIO VENTA']}</p>
        </div>
        <a href="../index.html">Volver a la tienda</a>
        <script>
            document.querySelectorAll('img[id$="_cover"], img[id$="_back"], img[id$="_in"]').forEach(img => {{
                img.onclick = function() {{
                    document.getElementById('imgModal').src = this.src;
                    document.getElementById('modal').style.display = "block";
                }};
            }});
            document.getElementById('cerrar').onclick = function() {{
                document.getElementById('modal').style.display = "none";
            }};
            window.onclick = function(event) {{
                if (event.target == document.getElementById('modal')) {{
                    document.getElementById('modal').style.display = "none";
                }}
            }};
        </script>
    </body>
    </html>
    """

    # Guardar el archivo HTML
    with open(f'catálogo/{title}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Suponiendo que las columnas se llaman 'TÍTULO', 'PRECIO VENTA' 
libros = df[['TÍTULO', 'PRECIO VENTA']].values.tolist()

# Imagen predeterminada si no hay imagen disponible
imagen_predeterminada = 'agua_sabajo_logo.png'

# Generar el contenido HTML para los productos
productos_html = ''
for titulo, precio in libros:
    # Reemplazar espacios por guiones bajos en el título para el enlace
    titulo_enlace = titulo.replace(' ', '_')
    
    productos_html += f'''
        <div class="producto">
            <a href="catálogo/{titulo_enlace}.html">
                <img src="img/{titulo_enlace}_cover.jpg" alt="Portada {titulo}" width="50" height="50">
            </a><br>
            <span>{titulo}<br> <strong>${precio}</strong></span><br>
            <button onclick="agregarAlCarrito('{titulo}', {precio})">Añadir</button>
        </div>\n
    '''

# Leer el contenido de index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Modificar solo el contenido del div con id="productos"
# Reemplazar el contenido previo del div
new_content = re.sub(r'<!-- INICIO -->.*?<!-- FIN -->', f'<!-- INICIO -->\n{productos_html}<!-- FIN -->', index_content, flags=re.DOTALL)

# Guardar el contenido actualizado en index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("El contenido del div 'productos' en index.html ha sido actualizado.")

