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
    title = row['TÍTULO'].replace(' ', '_')  # Reemplazar espacios en el título con guiones bajos
    isbn_value = str(int(row['ISBN'])) if row['ISBN'] != "No disponible" else "No disponible"
    year_value = str(int(row['AÑO'])) if row['AÑO'] != "No disponible" else "No disponible"

    html_content = f'''
    <html>
    <head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{row["TÍTULO"]}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
        <style> body {{ font-family: 'Atkinson Hyperlegible', sans-serif; }}</style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center">{row["TÍTULO"]}</h1>
            <div class="text-center">
                <img id="{title}_cover" src="../img/{title}_cover.jpg" width="300" alt="Portada" style="cursor:pointer;">
                <img id="{title}_back" src="../img/{title}_back.jpg" width="300" alt="Contraportada" style="cursor:pointer;">
                <img id="{title}_in" src="../img/{title}_in.jpg" width="300" alt="Interior" style="cursor:pointer;">
            </div>
            <div class="info text-center">
                <p><strong>Autor:</strong> {row["AUTOR"]}</p>
                <p><strong>Año:</strong> {year_value}</p>
                <p><strong>ISBN:</strong> {isbn_value}</p>
                <p><strong>Editorial:</strong> {row["EDITORIAL"]}</p>
                <p><strong>Precio:</strong> ${row["PRECIO VENTA"]}</p>
            </div>
            <a href="../index.html" class="btn btn-primary">Volver a la tienda</a>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="imageModal" tabindex="-1" role="dialog" aria-labelledby="modalTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalTitle">Imagen</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body text-center">
                        <img id="imgModal" src="" class="img-fluid" alt="Imagen del libro">
                    </div>
                    <div class="modal-footer">
                        <button id="prevBtn" class="btn btn-secondary" style="display:none;">Anterior</button>
                        <button id="nextBtn" class="btn btn-secondary" style="display:none;">Siguiente</button>
                        <button type="button" class="btn btn-danger" data-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
        
<script>
    let currentIndex = 0; 
    const images = []; 

    // Llenar el array images cuando se asignan los manejadores de eventos
    document.querySelectorAll('img[id$="_cover"], img[id$="_back"], img[id$="_in"]').forEach((img, index) => {{
        images.push(img.src);  // Agregar cada imagen al array en la inicialización
        img.onclick = function() {{
            currentIndex = index; 
            document.getElementById('imgModal').src = this.src; 
            $('#imageModal').modal('show'); 
            checkButtons(); 
        }};
    }});

    document.getElementById('prevBtn').onclick = function() {{
        if (currentIndex > 0) {{
            currentIndex--;
            updateModalImage();
        }}
    }};

    document.getElementById('nextBtn').onclick = function() {{
        if (currentIndex < images.length - 1) {{
            currentIndex++;
            updateModalImage();
        }}
    }};

    function updateModalImage() {{
        document.getElementById('imgModal').src = images[currentIndex]; 
        checkButtons(); 
    }}

    function checkButtons() {{
        document.getElementById('prevBtn').style.display = currentIndex === 0 ? 'none' : 'inline'; 
        document.getElementById('nextBtn').style.display = currentIndex === images.length - 1 ? 'none' : 'inline'; 
    }}
</script>

    </body>
    </html>
    '''

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
    titulo_enlace = titulo.replace(' ', '_')
    
    productos_html += f'''
        <div class="producto">
            <a href="catálogo/{titulo_enlace}.html">
                <img src="img/{titulo_enlace}_cover.jpg" alt="Portada {titulo}" width="50" height="50">
            </a><br>
            <span>{titulo}<br> <strong>${precio}</strong></span><br>
            <button onclick="agregarAlCarrito('{titulo}', {precio})" class="btn btn-success">Añadir</button>
        </div>
    '''

# Leer el contenido de index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Modificar el contenido del div con id="productos"
# Reemplazar el contenido previo del div
new_content = re.sub(r'<!-- INICIO -->.*?<!-- FIN -->', f'<!-- INICIO -->\n{productos_html}<!-- FIN -->', index_content, flags=re.DOTALL)

# Guardar el contenido actualizado en index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("El contenido del div 'productos' en index.html ha sido actualizado.")


