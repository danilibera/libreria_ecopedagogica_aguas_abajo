import pandas as pd
import os
import re

# Cargar el archivo XLS
df = pd.read_excel('LIBRERÍA_AGUAS_ABAJO.xlsx')

# Seleccionar las columnas necesarias y manejar NaN
df = df[['TÍTULO', 'AUTOR', 'AÑO', 'ISBN', 'EDITORIAL', 'PRECIO VENTA']].fillna({
    'ISBN': "No disponible",
    'AÑO': "No disponible"
})

# Generar el contenido HTML para los productos
productos_html = ''
for index, row in df.iterrows():
    titulo = row['TÍTULO'].replace(' ', '_')
    precio = row['PRECIO VENTA']
    autor = row['AUTOR']
    año = str(int(row['AÑO'])) if row['AÑO'] != "No disponible" else "No disponible"
    isbn = row['ISBN']
    editorial = row['EDITORIAL']
    
    # Generar HTML para cada producto
    productos_html += f'''
        <div class="col-md-4">
            <div class="producto">
                <img src="img/{titulo}_cover.jpg" alt="Portada {row['TÍTULO']}"
                     onclick="mostrarInfo('{row['TÍTULO']}', '{autor}', '{año}', '{isbn}', '{editorial}', {precio},
                     'img/{titulo}_cover.jpg', 'img/{titulo}_back.jpg', 'img/{titulo}_in.jpg')">
                <span>{row['TÍTULO']}<br> <strong>${precio}</strong></span><br>
                <button onclick="agregarAlCarrito('{row['TÍTULO']}', {precio})">Añadir</button>
            </div>
        </div>
    '''

# Leer el contenido de index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Modificar el contenido del div con id="productos"
new_content = re.sub(r'<!-- INICIO -->.*?<!-- FIN -->', f'<!-- INICIO -->\n{productos_html}<!-- FIN -->', index_content, flags=re.DOTALL)

# Guardar el contenido actualizado en index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("El contenido del div 'productos' en index.html ha sido actualizado.")
