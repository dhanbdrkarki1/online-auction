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
      {
        data: 'shipping_status',
        render: function (data) {
          var status = '';
          if (data === 'pending') {
            status = 'Pending';
          } else if (data === 'in_transit') {
            status = 'In Transit';
          } else if (data === 'delivered') {
            status = 'Delivered';
          }
          return status;
        },
      },

      {
        data: 'id',
        render: function (data, type, row) {
          var elem = '';
          if (row.shipping_status === 'delivered') {
            elem = `<div class="w-75 btn-group" role="group">
                      <a href="/lots/${row.slug}/" class="btn btn-secondary mx-2"> <i class="bi bi-eye-fill"></i> </a>
                    </div>`;
          } else {
            elem = `<div class="w-75 btn-group" role="group">
                        <a href="#" class="btn btn-primary mx-2" id="markedAsDeliveredBtn" data-shipment-id="${row.shipment_id}" > Mark as Delivered </a>
                        <a href="/lots/${row.slug}/" class="btn btn-secondary mx-2"> <i class="bi bi-eye-fill"></i> </a>
                      </div>`;
          }
          return elem;
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

  $('#tblPaidLots').on('click', '#markedAsDeliveredBtn', function () {
    const csrftoken = Cookies.get('csrftoken');
    var shipmentUpdateUrl = '/api/lots/ship/update/';
    var shipmentId = $(this).data('shipment-id');

    fetch(shipmentUpdateUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        shipment_id: shipmentId,
        shipment_date: '',
        shipment_status: 'delivered',
      }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        toastr.success(data['message']);
        // Reload table after successful update
        reloadPaidLotsDataTable();

        console.log('Shipment updated successfully:');
      })
      .catch((error) => {
        toastr.error(data['error']);
        console.error('Error updating shipment:', error);
      });
  });

  // reloading table
  function reloadPaidLotsDataTable() {
    if ($.fn.DataTable.isDataTable('#tblPaidLots')) {
      $('#tblPaidLots').DataTable().ajax.reload();
    }
  }
}
