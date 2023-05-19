function generarTablaTipoProductos(tipo_producto) {
  $("#myTable").bootstrapTable({
    url: "/get_productos",
    queryParams: function(params) {
      // Agregar el parámetro "tipo_producto" con el valor seleccionado
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
    //paginationVAlign: "both",
    showCustomView: true,
    onLoadSuccess: (number, size) => {
      $("#divTabla").show();
      $("[name='customView']").click().remove();
      $(".progress, .fixed-table-body, .pagination-detail").hide();
    },
    onLoadError: (status, res) => {
      // Ocultamos el indicador de carga en caso de que haya un error
      console.log(res.statusText, res.status);
      console.log(res.responseText);
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
            row.nombre.length > 50
              ? row.nombre.substring(0, 50) + "..."
              : row.nombre
          )
          .replaceAll("%nombre%", row.nombre)
          .replaceAll("%photo%", row.photo)
          .replaceAll("%precio%", row.precio)
          .replaceAll("%format_clp%", row.format_clp)
          .replaceAll("%marca%", row.marca);
      });
      // Retornamos un row con colum
      return `<div style="margin-top:30px;" class="row mt-5">${view}</div>`;
    },
  });
}
