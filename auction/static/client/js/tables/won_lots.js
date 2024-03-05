// var dataTable;
// $(document).ready(function () {
//   loadDataTable();
// });

// function loadDataTable() {
//   dataTable = $('#wonLotsTable').DataTable({
//     ajax: { url: '/api/lots/won' },
//     columns: [
//       { data: 'id', width: '20%' },
//       { data: 'name', width: '10%' },
//       { data: 'highest_bid_amount', width: '30%' },
//       { data: 'starting_price', width: '10%' },
//       { data: 'auction_duration', width: '10%' },

//       //   { data: 'price', width: '10%' },
//       //   { data: 'stockQuantity', width: '10%' },
//       //   {
//       //     data: 'createdDate',
//       //     render: function (data) {
//       //       return formatDateTime(data);
//       //     },
//       //     width: '15%',
//       //   },
//       //   {
//       //     data: 'modifiedDate',
//       //     render: function (data) {
//       //       return formatDateTime(data);
//       //     },
//       //     width: '15%',
//       //   },
//       //   {
//       //     data: 'productId',
//       //     render: function (data) {
//       //       return `<div class="w-75 btn-group" role="group">
//       //                     <a href="/admin/product/upsert?id=${data}" class="btn btn-primary mx-2"> <i class="bi bi-pencil-square"></i> Edit </a>
//       //                     <a onClick=Delete('/admin/product/delete?id=${data}') class="btn btn-danger mx-2"> <i class="bi bi-trash-fill"></i> Delete </a>
//       //                     </div>
//       //                 `;
//       //     },
//       //     width: '15%',
//       //   },
//     ],
//     responsive: true,
//     searching: false,
//     paging: false,
//     info: false,
//   });
// }

// function Delete(url) {
//   Swal.fire({
//     title: 'Are you sure?',
//     text: "You won't be able to revert this!",
//     icon: 'warning',
//     showCancelButton: true,
//     confirmButtonColor: '#3085d6',
//     cancelButtonColor: '#d33',
//     confirmButtonText: 'Yes, delete it!',
//   }).then((result) => {
//     if (result.isConfirmed) {
//       $.ajax({
//         url: url,
//         type: 'DELETE',
//         success: function (data) {
//           dataTable.ajax.reload();
//           toaster.success(data.message);
//         },
//       });
//     }
//   });
// }

var dataTable;

$(document).ready(function () {
  loadDataTable();
});

function loadDataTable() {
  dataTable = $('#tblLotsWon').DataTable({
    ajax: {
      url: '/api/lots/won',
      dataSrc: '',
    },
    columns: [
      {
        data: 'name',
        render: function (data, type, row) {
          return '<a href="/lots/' + row.slug + '/' + '">' + data + '</a>';
        },
      },
      { data: 'highest_bid_amount' },
      { data: 'starting_price' },
      { data: 'auction_duration' },
      {
        data: 'auction_start_time',
        render: function (data) {
          return formatDateTime(data);
        },
      },
      {
        data: 'id',
        render: function (data, type, row) {
          return `<div class="w-75 btn-group" role="group">
                                <button type="button" class="btn btn-primary mx-2 payment-button" data-lot-id="${row.id}"> <i class="bi bi-cash"></i> Pay Now </button>
                                <a href="/lots/${row.slug}/" class="btn btn-secondary mx-2"> <i class="bi bi-eye-fill"></i> View </a>
                                </div>
                            `;
        },
        width: '15%',
      },
    ],
    responsive: true,
    searching: false,
    paging: false,
    info: false,
    language: {
      emptyTable: 'No data available in table',
    },
  });

  // Handle click on Pay Now button
  $('#tblLotsWon').on('click', '.payment-button', function () {
    var lotId = $(this).data('lot-id');
    $('#paymentModal').modal('show');
    $('#paymentModal').find('.payment-option').data('lot-id', lotId);
  });

  // Handle click on payment option
  $('.payment-option').click(function () {
    var paymentType = $(this).data('payment');
    var lotId = $(this).data('lot-id');
    $('#paymentModal').modal('hide');
    payWithPaymentType(paymentType, lotId);
  });

  function payWithPaymentType(paymentType, lotId) {
    console.log(
      'Processing payment with ' + paymentType + ' for lot ID ' + lotId
    );
  }
}
