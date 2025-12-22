import os
import pandas as pd
import re
import html 


def esc(s):
    s = str(s)
    s = s.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ")
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return html.escape(s, quote=True)


# Carpeta de imágenes y logo placeholder 
img_folder = "img"
logo_placeholder = "agua_sabajo_logo.png"  # está en la raíz



# Cargar el archivo XLS
df = pd.read_excel('LIBRERÍA_AGUAS_ABAJO.xlsx')

# Seleccionar columnas necesarias y manejar NaN
df = df[['TÍTULO', 'AUTOR', 'AÑO', 'ISBN', 'EDITORIAL', 'RESUMEN', 'PRECIO VENTA']].fillna({
    'ISBN': "No disponible",
    'AÑO': "No disponible",
    'RESUMEN': "No disponible"
})

productos_html = ''
for index, row in df.iterrows():
    # Escapar textos
    titulo = esc(row['TÍTULO'])
    autor = esc(row['AUTOR'])
    editorial = esc(row['EDITORIAL'])
    resumen = esc(row['RESUMEN'])
    isbn = esc(row['ISBN'])

    # Año robusto
    if row['AÑO'] == "No disponible":
        año = "No disponible"
    else:
        try:
            año = str(int(float(row['AÑO'])))
        except Exception:
            año = esc(row['AÑO'])

    # Precio robusto
    try:
        precio = int(float(row['PRECIO VENTA']))
    except Exception:
        precio = 0

    # Nombre de archivo (manteniendo guiones bajos)
    titulo_slug = str(row['TÍTULO']).replace(" ", "_")

    # Rutas de imágenes
    cover_path = f"{img_folder}/{titulo_slug}_cover.jpg"
    back_path  = f"{img_folder}/{titulo_slug}_back.jpg"
    in_path    = f"{img_folder}/{titulo_slug}_in.jpg"

    # Si no existen, usar logo como placeholder
    if not os.path.exists(cover_path):
        cover_path = logo_placeholder
    if not os.path.exists(back_path):
        back_path = logo_placeholder
    if not os.path.exists(in_path):
        in_path = logo_placeholder

    # Generar HTML para cada producto con data-attributes
    productos_html += f'''
        <div class="col-md-4">
            <div class="producto">
                <img
                    src="{cover_path}"
                    alt="Portada {titulo}"
                    data-titulo="{titulo}"
                    data-autor="{autor}"
                    data-anio="{año}"
                    data-isbn="{isbn}"
                    data-editorial="{editorial}"
                    data-resumen="{resumen}"
                    data-precio="{precio}"
                    data-cover="{cover_path}"
                    data-back="{back_path}"
                    data-in="{in_path}"
                    onclick="mostrarInfo(this)"
                ><br>
                <span>{titulo}<br> <strong>${precio}</strong></span><br>
                <button onclick="agregarAlCarrito('{titulo}', {precio})">Añadir</button>
            </div>
        </div>
    '''

# Leer index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Reemplazar bloque entre <!-- INICIO --> y <!-- FIN -->
new_content = re.sub(
    r'<!-- INICIO -->.*?<!-- FIN -->',
    f'<!-- INICIO -->\n{productos_html}<!-- FIN -->',
    index_content,
    flags=re.DOTALL
)

# Guardar index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("El contenido del div 'productos' en index.html ha sido actualizado.")
