$(document).ready(function () {
  $('#nav-lot-shipment-tab').on('shown.bs.tab', function () {
    // Check if DataTable for lot shipment already exists
    if (!$.fn.DataTable.isDataTable('#tblLotShipment')) {
      loadLotShipmentTable();
    }
  });
});

function loadLotShipmentTable() {
  $('#tblLotShipment').DataTable({
    ajax: {
      url: '/api/lots/ship/list/',
      dataSrc: '',
    },
    columns: [
      {
        data: 'lot_name',
        render: function (data, type, row) {
          return '<a href="/lots/' + row.slug + '/' + '">' + data + '</a>';
        },
      },
      { data: 'payment_method' },
      {
        data: 'shipment_status',
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
        data: 'shipment_id',
        render: function (data, type, row) {
          var elem = '';
          if (row.shipment_status === 'delivered') {
            elem = `<div class="w-75 btn-group" role="group">
                      <a href="/lots/${row.slug}/" class="btn btn-secondary mx-2"> <i class="bi bi-eye-fill"></i> </a>
                    </div>`;
          } else {
            elem = `<div class="w-75 btn-group" role="group">
                    <button type="button" class="btn btn-primary mx-2 shipment-button" data-lot-name="${row.lot_name}" data-shipment-status="${row.shipment_status}" data-shipping-date=${row.shipping_date} data-shipment-id="${row.shipment_id}"> 
                    <i class="bi bi-truck"></i> 
                    Update Shipment </button>
                                </div>
                            `;
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
      emptyTable: "You don't have any lots ready to be shipped till yet...",
    },
  });

  // Handle click on Shipment button
  $('#tblLotShipment').on('click', '.shipment-button', function () {
    var shipmentId = $(this).data('shipment-id');
    var shipmentStatus = $(this).data('shipment-status');
    var lot_name = $(this).data('lot-name');
    var shipping_date = $(this).data('shipping-date');
    shipping_date = moment(shipping_date).format('YYYY/MM/DD HH:mm:ss');
    console.log(shipping_date);

    console.log(shipmentId, shipmentStatus, lot_name, shipping_date);

    $('#shipmentModal').modal('show');

    $('#shippingLotName').val(lot_name);
    if (shipping_date !== '') {
      $('.datetimepicker-input').val(shipping_date);
    }
    var $shipmentStatusDropdown = $('#shipmentStatus');
    $shipmentStatusDropdown.empty();

    var statusOptions = {
      pending: 'Pending',
      in_transit: 'In Transit',
      cancelled: 'Cancelled',
    };

    $.each(statusOptions, function (value, text) {
      var $option = $('<option>', {
        value: value,
        text: text,
      });

      if (shipmentStatus === value) {
        // Select the option if it matches the shipment status
        $option.attr('selected', true);
      }
      // Append the option to the dropdown
      $shipmentStatusDropdown.append($option);
    });

    $('#shipmentModal')
      .find('.update-shipment')
      .data('shipment-id', shipmentId);
  });

  $('.update-shipment').click(function (e) {
    e.preventDefault();
    var shipmentId = $(this).data('shipment-id');
    var shipmentStatus = $('#shipmentStatus').val();
    var shipmentDate = $('.datetimepicker-input').val();

    $('#shipmentModal').modal('hide');

    var shipmentUpdateUrl = '/api/lots/ship/update/';
    const csrftoken = Cookies.get('csrftoken');

    fetch(shipmentUpdateUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        shipment_id: shipmentId,
        shipment_date: shipmentDate,
        shipment_status: shipmentStatus,
      }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        toastr.success(data['message']);
        // Reload table after successful update
        reloadLotShipmentTable();

        console.log('Shipment updated successfully:');
      })
      .catch((error) => {
        toastr.error(data['error']);
        console.error('Error updating shipment:', error);
      });
  });

  // reloading table
  function reloadLotShipmentTable() {
    if ($.fn.DataTable.isDataTable('#tblLotShipment')) {
      $('#tblLotShipment').DataTable().ajax.reload();
    }
  }
}
