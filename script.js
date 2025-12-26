/* ============================
   Variables globales
============================ */
let images = [];
let currentIndex = 0;
let carrito = [];
let total = 0;

/* ============================
   Carrito de compras
============================ */
function agregarAlCarrito(nombre, precio) {
    const itemExistente = carrito.find(item => item.nombre === nombre);

    if (itemExistente) {
        itemExistente.cantidad++;
    } else {
        carrito.push({ nombre, precio, cantidad: 1 });
    }
    total += precio;
    actualizarCarrito();
}

function eliminarDelCarrito(nombre) {
    const itemIndex = carrito.findIndex(item => item.nombre === nombre);

    if (itemIndex !== -1) {
        total -= carrito[itemIndex].precio;
        if (carrito[itemIndex].cantidad > 1) {
            carrito[itemIndex].cantidad--;
        } else {
            carrito.splice(itemIndex, 1);
        }
        actualizarCarrito();
    }
}

function actualizarCarrito() {
    const lista = document.getElementById("listaCarrito");
    const totalElemento = document.getElementById("total");
    const detallesPedido = document.getElementById("detallesPedido");
    const carritoTexto = [];

    lista.innerHTML = "";
    detallesPedido.innerHTML = "";

    carrito.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.nombre} - CLP ${item.precio} (Cantidad: ${item.cantidad}) `;

        const botonEliminar = document.createElement("button");
        botonEliminar.textContent = "Eliminar";
        botonEliminar.onclick = () => eliminarDelCarrito(item.nombre);
        li.appendChild(botonEliminar);

        lista.appendChild(li);
        detallesPedido.innerHTML += `${item.nombre} - CLP ${item.precio} (Cantidad: ${item.cantidad})<br>`;
        carritoTexto.push(`${item.nombre} - CLP ${item.precio} (Cantidad: ${item.cantidad})`);
    });

    totalElemento.textContent = total;
    document.getElementById("carrito").value = carritoTexto.join(', ');
    document.getElementById("totalPedido").value = total;
    document.getElementById("totalVisible").textContent = total;
}

/* ============================
   Modal de producto
============================ */
function mostrarInfo(el) {
    const d = el.dataset;

    // Imagen principal
    document.getElementById('imgModal').src = d.cover;

    // Info textual
    document.getElementById('modalAuthor').textContent = "Autor: " + d.autor;
    document.getElementById('modalYear').textContent = "Año: " + d.anio;
    document.getElementById('modalISBN').textContent = "ISBN: " + d.isbn;
    document.getElementById('modalEditorial').textContent = "Editorial: " + d.editorial;
    document.getElementById('modalDescription').textContent = d.resumen;
    document.getElementById('modalPrice').textContent = "Precio: $" + d.precio;

    // Navegación de imágenes
    images = [d.cover, d.back, d.in].filter(src => src && src !== "");
    currentIndex = 0;

    checkButtons();
    document.getElementById('prevBtn').onclick = prevImage;
    document.getElementById('nextBtn').onclick = nextImage;

    // Mostrar modal (Bootstrap)
    $('#imageModal').modal('show');
}

function updateModalImage() {
    document.getElementById('imgModal').src = images[currentIndex];
    checkButtons();
}

function prevImage() {
    if (currentIndex > 0) {
        currentIndex--;
        updateModalImage();
    }
}

function nextImage() {
    if (currentIndex < images.length - 1) {
        currentIndex++;
        updateModalImage();
    }
}

function checkButtons() {
    document.getElementById('prevBtn').style.display = currentIndex === 0 ? 'none' : 'inline';
    document.getElementById('nextBtn').style.display = currentIndex === images.length - 1 ? 'none' : 'inline';
}

/* ============================
   Formulario de contacto
============================ */
document.getElementById('formContacto').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        alert('Formulario enviado. ¡Gracias por tu pedido! Recibirás un correo con detalles de pago y opciones de envío');
        this.reset();
        carrito = [];
        total = 0;
        actualizarCarrito();
    })
    .catch(error => {
        alert('Hubo un problema al enviar el formulario. Por favor, inténtalo de nuevo.');
        console.error('Error:', error);
    });
});

/* ============================
   Scroll suave a contacto
============================ */
function scrollToContacto() {
    document.getElementById('contacto').scrollIntoView({ behavior: 'smooth' });
}
