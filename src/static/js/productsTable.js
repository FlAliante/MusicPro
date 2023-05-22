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
  $(".fixed-table-body").hide()
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
  $(".fixed-table-body").hide()
}