import pandas as pd
import os
import re

# Cargar el archivo XLS
df = pd.read_excel('LIBRERÍA_AGUAS_ABAJO.xlsx')

# Seleccionar las columnas necesarias
df = df[['TÍTULO', 'AUTOR', 'AÑO', 'ISBN', 'EDITORIAL', 'PRECIO VENTA']]

# Crear una carpeta para las páginas
os.makedirs('catálogo', exist_ok=True)

# Generar las páginas HTML
for index, fila in df.iterrows():
    html_content = f"""
    <html>
    <head>
        <title>{fila['TÍTULO']}</title>
        <style>
            body {{
                font-family: Atkinson hyperlegible, sans-serif;
                text-align: center;
                margin: 20px;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            h1 {{
                color: #333;
            }}
            .info {{
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #fff;
            }}
        </style>
    </head>
    <body>
		<img src="../img/{fila['TÍTULO'].replace(" ", "_")}.jpg" width="300">
        <h1>{fila['TÍTULO']}</h1>
        <div class="info">
            <p><strong>Autor:</strong> {fila['AUTOR']}</p>
            <p><strong>Año:</strong> {fila['AÑO']}</p>
            <p><strong>ISBN:</strong> {fila['ISBN']}</p>
            <p><strong>Editorial:</strong> {fila['EDITORIAL']}</p>
            <p><strong>Precio:</strong> ${fila['PRECIO VENTA']}</p>
        </div>
        <!-- Botón para volver a la tienda -->
    <br><br>
    <a href="../index.html">Volver a la tienda</a>
    </body>
    </html>
    """
    # Guardar el archivo HTML
    with open(f'catálogo/{fila["TÍTULO"].replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
# Suponiendo que las columnas se llaman 'TÍTULO', 'PRECIO VENTA' e 'IMAGEN'
libros = df[['TÍTULO', 'PRECIO VENTA']].values.tolist()
        
# Imagen predeterminada si no hay imagen disponible
imagen_predeterminada = 'agua_sabajo_logo.png'  

# Generar el contenido HTML para los productos
productos_html = ''
for titulo, precio in libros:
    # Reemplazar espacios por guiones bajos en el título para el enlace
    titulo_enlace = titulo.replace(' ', '_')
    
    # Usar la imagen predeterminada si no hay imagen
   # if pd.isna(imagen) or imagen.strip() == '':
    #    imagen = imagen_predeterminada
    
    productos_html += f'''
        <div class="producto">
            <a href="catálogo/{titulo_enlace}.html">
                <img src="img/{titulo_enlace}.jpg" alt="Portada {titulo} "width="50" height="50">
            </a></br>
            <span>{titulo} </br> <strong>${precio}</strong></span></br>
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
