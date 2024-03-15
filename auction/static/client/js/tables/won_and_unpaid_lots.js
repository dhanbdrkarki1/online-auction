var dataTable;

$(document).ready(function () {
  loadUnpaidLotsDataTable();
});

function loadUnpaidLotsDataTable() {
  dataTable = $('#tblUnpaidLots').DataTable({
    ajax: {
      url: '/api/lots/won/unpaid',
      dataSrc: '',
    },
    columns: [
      {
        data: 'name',
        render: function (data, type, row) {
          return '<a href="/lots/' + row.slug + '/' + '">' + data + '</a>';
        },
        width: '15%',
      },
      { data: 'highest_bid_amount' },
      {
        data: 'auction_start_time',
        render: function (data) {
          return formatDateTime(data);
        },
      },
      { data: 'auction_duration' },

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
      emptyTable: 'No lot has been won till yet..',
    },
  });

  // Handle click on Pay Now button
  $('#tblUnpaidLots').on('click', '.payment-button', function () {
    var lotId = $(this).data('lot-id');
    var highestBidAmount = $(this).data('highest-bid-amount');
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
