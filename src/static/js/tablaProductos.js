var carrito_total = localStorage.getItem("carrito_total");
var carrito_item = localStorage.getItem("carrito_item");
var compra_formato = localStorage.getItem("compra_formato");
var carrito_productos = localStorage.getItem("carrito_productos");
var formatter = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
});

function agregarAlCarrito(precio, description, photo, id) {
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
    description: description,
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

function limpiarCarrito() {
  carrito_total = 0;
  carrito_item = 0;
  carrito_productos = "[]";

  localStorage.setItem("carrito_total", carrito_total);
  localStorage.setItem("carrito_item", carrito_item);
  localStorage.setItem("carrito_productos", carrito_productos);

  $("#carrito_total").text("$" + carrito_total);
  $("#carrito_item").text(carrito_item);
}

size_nombre_sort = 50;

function generarTablaTipoProductos(tipo_producto) {
  $("#myTable").bootstrapTable({
    url: "https://music-pro-api.herokuapp.com/api/get_productos",
    queryParams: function (params) {
      // Agregar el parámetro "?tipo_producto=" con el valor del parametro
      params.tipo_producto = tipo_producto;
      return params;
    },
    locale: "es-CL",
    search: true,
    columns: [{ field: "nombre", sortable: true }],
    searchAlign: "left",
    pageSize: 8,
    pagination: true,
    paginationPreText: "Anterior",
    paginationNextText: "Siguiente",
    pageList: "[All]",
    //paginationVAlign: "both",
    showCustomView: true,
    onLoadSuccess: (number, size) => {
      $(".progress").hide();
      $("#divTabla").show();
    },
    onLoadError: (status, res) => {
      // Ocultamos el indicador de carga en caso de que haya un error
      console.error(res);
      $("#txtError").text(`${res.statusText}(${res.status})`);
      $(".progress").hide();
      $(".alert-danger").show();
    },
    onPageChange: (number, size) => {
      window.scrollTo(0, 0);
    },
    customView: (data) => {
      // Agregamos el HTML para cargar los datos
      var view = "";
      var template = $("#tableTemplate").html();
      var nombre_sort = "";
      // Recorremos datos
      $.each(data, function (i, row) {
        view += template
          .replaceAll(
            "%nombre_sort%",
            row.nombre.length > size_nombre_sort
              ? row.nombre.substring(0, size_nombre_sort) + "..."
              : row.nombre
          )
          .replaceAll("%nombre%", row.nombre)
          .replaceAll("%photo%", row.photo)
          .replaceAll("%precio%", row.precio)
          .replaceAll("%format_clp%", row.format_clp)
          .replaceAll("%marca%", row.marca)
          .replaceAll("%id%", row.id);
      });
      // Retornamos un row con colum
      return `<div class="row">${view}</div>`;
    },
  });
}

function generarTablaProductoIndex() {
  $("#myTable").bootstrapTable({
    url: "https://music-pro-api.herokuapp.com/api/get_productos",
    locale: "es-CL",
    showCustomView: true,
    onLoadSuccess: function (number, size) {
      $(".progress").hide();
    },
    onPageChange: function (number, size) {
      window.scrollTo(0, 0);
    },
    customView: function (data) {
      // Agregamos el HTML para cargar los datos
      var view = "";
      var template = $("#tableTemplate").html();
      var nombre_sort = "";
      // Recorremos datos
      $.each(data, function (i, row) {
        nombre_sort =
          row.nombre.length > size_nombre_sort
            ? row.nombre.substring(0, size_nombre_sort) + "..."
            : row.nombre;
        view += template
          .replaceAll("%nombre_sort%", nombre_sort)
          .replaceAll("%nombre%", row.nombre)
          .replaceAll("%marca%", row.marca)
          .replaceAll("%photo%", row.photo)
          .replaceAll("%precio%", row.precio)
          .replaceAll("%format_clp%", row.format_clp)
          .replaceAll("%id%", row.id);
      });
      // Retornamos un row con colum
      return `<div class="row">${view}</div>`;
    },
  });
}



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
    $("#carrito_tabla, #carrito_item").hide();
    $("#carrito_msj").show();
  });
});
