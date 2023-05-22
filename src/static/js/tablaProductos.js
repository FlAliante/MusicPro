var compra_total = localStorage.getItem("compra_total");
var compra_item = localStorage.getItem("compra_item");
var compra_formato = localStorage.getItem("compra_formato");
var compra_productos = localStorage.getItem("compra_productos");
var formatter = new Intl.NumberFormat("es-CL", {
  style: "currency",
  currency: "CLP",
});

function agregarAlCarrito(precio, description, photo, id) {
  //parseo textos a numeros para sumar
  precio = parseInt(precio);
  compra_total = parseInt(compra_total);
  //Recupero txt y parseo a json
  compra_productos = JSON.parse(compra_productos);
  // Incrementa el número actual en 1 cada vez que se llama esta función
  compra_total += precio;
  compra_item++;
  // Crear un objeto para almacenar
  var objeto = {
    precio: precio,
    description: description,
    photo: photo,
    format: formatter.format(precio),
    id: id,
  };
  //Adjunto datos
  compra_productos.push(objeto);
  // Esto transforma a json tipo text. si no se guarda asi el array no se puede acceder despues
  compra_productos = JSON.stringify(compra_productos);
  // Escribe el nuevo número asignado en el almacenamiento local
  localStorage.setItem("compra_total", compra_total);
  localStorage.setItem("compra_item", compra_item);
  localStorage.setItem("compra_productos", compra_productos);
  // Actualiza el contenido del elemento HTML que muestra el número asignado
  $("#compra_total").text(formatter.format(compra_total));
  $("#compra_item").text(compra_item).show();
}

function limpiarCarrito() {
  compra_total = 0;
  compra_item = 0;
  compra_productos = "[]";

  localStorage.setItem("compra_total", compra_total);
  localStorage.setItem("compra_item", compra_item);
  localStorage.setItem("compra_productos", compra_productos);

  $("#compra_total").text("$" + compra_total);
  $("#compra_item").text(compra_item);
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
  if (!compra_item) {
    compra_total = 0;
    compra_item = 0;
    compra_productos = "[]";
  }

  $("#compra_total").text(formatter.format(compra_total));
  $("#compra_item").text(compra_item);

  if ($("#compra_item").text() != 0) {
    $("#compra_item").show();
  }

  $("#vaciar_carrito").on("click", function () {
    $("#carrito_tabla, #compra_item").hide();
    $("#carrito_msj").show();
  });
});
