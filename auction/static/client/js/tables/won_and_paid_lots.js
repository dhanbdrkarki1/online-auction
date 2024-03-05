$(document).ready(function () {
  $('#paid-lots-tab').on('shown.bs.tab', function () {
    // Check if DataTable for paid lots already exists
    if (!$.fn.DataTable.isDataTable('#tblPaidLots')) {
      loadPaidLotsDataTable();
    }
  });
});

function loadPaidLotsDataTable() {
  $('#tblPaidLots').DataTable({
    ajax: {
      url: '/api/lots/won/paid',
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
      { data: 'payment_method' },
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
      emptyTable: 'No payment has been made till yet...',
    },
  });
}
