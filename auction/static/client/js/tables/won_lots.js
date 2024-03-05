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
                                <button type="button" class="btn btn-primary mx-2 payment-button" data-lot-id="${row.id}" data-highest-bid-amount="${row.highest_bid_amount}"> <i class="bi bi-cash"></i> Pay Now </button>
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
    var highestBidAmount = $(this).data('highest-bid-amount'); // Define highestBidAmount here
    $('#paymentModal').modal('show');
    $('#paymentModal').find('.payment-option').data('lot-id', lotId);
    $('#paymentModal')
      .find('.payment-option')
      .data('highest-bid-amount', highestBidAmount);
  });

  // Handle click on payment option
  $('.payment-option').click(function () {
    var paymentType = $(this).data('payment');
    var lotId = $(this).data('lot-id');
    var highestBidAmount = $(this).data('highest-bid-amount');

    $('#paymentModal').modal('hide');

    payWithPaymentType(paymentType, lotId, highestBidAmount);
  });

  function payWithPaymentType(paymentType, lotId, highestBidAmount) {
    console.log(
      'Processing payment with ' +
        paymentType +
        ' for lot ID ' +
        lotId +
        ' with highest bid amount ' +
        highestBidAmount
    );
    window.location.href = `/payment/request/${paymentType}/?lot_id=${lotId}&amount=${highestBidAmount}`;
  }
}
