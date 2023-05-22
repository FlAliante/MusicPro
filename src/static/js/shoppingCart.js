var carrito_total = localStorage.getItem("carrito_total");
var carrito_item = localStorage.getItem("carrito_item");
var carrito_productos = localStorage.getItem("carrito_productos");
var amount = carrito_total;
var formatter = new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
});


generarTablaCarrito = () => {
    // Parsear el string JSON a un objeto JavaScript con datos del carrito
    var productos = JSON.parse(carrito_productos);
    //Crea la tabla con datos del carrito
    if (productos.length > 0) {
        $('#carrito_tabla').show()
        // Seleccionar la tabla por su clase (en este caso, se usa la clase "table")
        var tabla = $('#tabla');
        var html = '';
        // Iterar sobre los elementos del array con forEach()
        productos.forEach(function (producto, indice) {
            html = $('#miNuevoElemento').html()
                .replaceAll('%format%', producto.format)
                .replaceAll('%nombre%', producto.nombre)
                .replaceAll('%photo%', producto.photo)
            tabla.append(html);
        });
        $('#amount').text(`CLP ${$('#carrito_total').text()} `)
        $('#carrito_botones').show();
        $("#amount_clp").val($('#carrito_total').text())
    } else {
        $('#carrito_msj').show();
    }
}

agregarAlCarrito = (precio, nombre, photo, id) => {
    //parseo textos a numeros para sumar
    precio = parseInt(precio);
    carrito_total = parseInt(carrito_total);
    //Recupero txt y parseo a json
    carrito_productos = JSON.parse(carrito_productos);
    // Incrementa el número actual en 1 cada vez que se llama esta función
    carrito_total += precio;
    carrito_item++;
    // Crear un objeto para almacenar
    var objeto = {
        precio: precio,
        nombre: nombre,
        photo: photo,
        format: formatter.format(precio),
        id: id,
    };
    //Adjunto datos
    carrito_productos.push(objeto);
    // Esto transforma a json tipo text. si no se guarda asi el array no se puede acceder despues
    carrito_productos = JSON.stringify(carrito_productos);
    // Escribe el nuevo número asignado en el almacenamiento local
    localStorage.setItem("carrito_total", carrito_total);
    localStorage.setItem("carrito_item", carrito_item);
    localStorage.setItem("carrito_productos", carrito_productos);
    // Actualiza el contenido del elemento HTML que muestra el número asignado
    $("#carrito_total").text(formatter.format(carrito_total));
    $("#carrito_item").text(carrito_item).show();
}



// Crea el pago
generarBotonPagar = () => $("#btn_pagar").on("click", function () {
    //Escondo botones
    $("#carrito_botones, .alert-danger").hide();
    $("#carrito_progress, #amount_retart").show();
    //Realizo llamado para consultar el codigo del producto
    $.ajax({
        method: "POST",
        url: "/transaction_create",
        dataType: "json",
        data: {
            amount: amount
        },
    }).done(function (response) {
        //recibo el numero de orden y hago el submit para el redirect
        $("#url").val(response.url);
        $("#token").val(response.token);
        $("#carrito_productos").val(carrito_productos);
        $("#formulario").submit();
    }).fail(function (jqXHR, textStatus) {
        console.error(jqXHR.responseText);
        $("#txtError").text(`${jqXHR.statusText} (${jqXHR.status})`);
        $(".alert-danger").show();
        $("#carrito_botones").show();
        $("#carrito_progress").hide();
    }).always(function () {
        console.log("Petición AJAX completada.");
    });
});

generarBotonUSD = () => $("#btn_usd").on("click", function () {
    //Escondo botones
    $("#carrito_botones, .alert-danger").hide();
    $("#carrito_progress, #amount_retart").show();

    $.ajax({
        url: "https://music-pro-api.herokuapp.com/api/exchange_rate",
        data: { amount_clp: carrito_total },
    }).done(function (response) {
        // Haz algo con la respuesta...
        $("#amount").text("USD " + response.format);
        $("#amount_usd").val(response.format);
        //amount = response.result
    }).fail(function (jqXHR, textStatus) {
        console.error(textStatus);
        console.error(jqXHR);
        $("#txtError").text(
            `${jqXHR.statusText}(${jqXHR.status}): ${jqXHR.responseText}`
        );
        $(".alert-danger").show();
    }).always(function () {
        $("#btn_usd, #carrito_progress, #amount_retart").hide();
        $("#btn_clp, #carrito_botones").show();
    });
});

generarBotonCLP = () => $("#btn_clp").on("click", function () {
    $("#carrito_progress, #amount_retart").show();
    $("#carrito_botones, .alert-danger").hide();
    // Agrega un retraso de 2 segundos
    // Agrega las funciones a la cola
    $("#btn_clp, #btn_usd").delay(600).queue(function (next) {
        $("#amount").text("CLP " + $("#carrito_total").text());
        $("#btn_clp, #carrito_progress, #amount_retart").hide();
        $("#btn_usd, #carrito_botones").show();
        amount = carrito_total;
        next();
    });
});

$(function () {
    // Si no hay un número previo en el almacenamiento local, establece el número inicial en 0
    if (!carrito_item) {
        carrito_total = 0;
        carrito_item = 0;
        carrito_productos = "[]";
    }

    $("#carrito_total").text(formatter.format(carrito_total));
    $("#carrito_item").text(carrito_item);

    if ($("#carrito_item").text() != 0) {
        $("#carrito_item").show();
    }


    $("#vaciar_carrito").on("click", function () {
        carrito_total = 0;
        carrito_item = 0;
        carrito_productos = "[]";

        localStorage.setItem("carrito_total", carrito_total);
        localStorage.setItem("carrito_item", carrito_item);
        localStorage.setItem("carrito_productos", carrito_productos);

        $("#carrito_total").text("$" + carrito_total);
        $("#carrito_item").text(carrito_item);

        $("#carrito_tabla, #carrito_item").hide();
        $("#carrito_msj").show();
    });
});
