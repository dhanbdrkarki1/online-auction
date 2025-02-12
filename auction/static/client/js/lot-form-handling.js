$(document).ready(function () {
  console.log('jQuery loaded successfully.');

  ImgUpload();
});

// ------------------------------------
// multi step form handling start
// ------------------------------------

var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  var x = document.getElementsByClassName('step');
  // Check if the index 'n' is within the bounds of the 'x' array
  if (n >= 0 && n < x.length) {
    // Hide all steps
    for (var i = 0; i < x.length; i++) {
      x[i].style.display = 'none';
    }
    // Display the selected step
    x[n].style.display = 'block';

    // Fix Previous/Next buttons
    if (n == 0) {
      document.getElementById('prevBtn').style.display = 'none';
    } else {
      document.getElementById('prevBtn').style.display = 'inline';
    }
    if (n == x.length - 1) {
      document.getElementById('nextBtn').innerHTML = 'Submit';
    } else {
      document.getElementById('nextBtn').innerHTML = 'Next';
    }

    // Update step indicator
    fixStepIndicator(n);
  } else {
    console.error('Invalid tab index:', n);
  }
}

function nextPrev(n) {
  var x = document.getElementsByClassName('step');
  if (n == 1) {
    if (!validateForm()) return false; // Check if form is valid before proceeding to the next step
    // Validate the form synchronously
    // Hide the current tab:
    x[currentTab].style.display = 'none';
  }
  currentTab = currentTab + n;
  if (x.length === 6) {
    generatePreview();
  }
  if (currentTab >= x.length) {
    document.getElementById('lotForm').submit();
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  var x = document.getElementsByClassName('step');
  var y = x[currentTab].getElementsByTagName('input');
  var valid = true;

  // Reset validation classes for all input fields in the current tab:
  // for (var i = 0; i < y.length; i++) {
  //   y[i].classList.remove('invalid');
  // }

  // // A loop that checks every input field in the current tab:
  // for (var i = 0; i < y.length; i++) {
  //   // If a field is empty and not of type file...
  //   if (y[i].value.trim() === '' && y[i].type !== 'file' && y[i] !== 'radio') {
  //     // Add an "invalid" class to the field:
  //     y[i].classList.add('invalid');
  //     // Set the current valid status to false:
  //     valid = false;
  //   }
  // }

  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document
      .getElementsByClassName('stepIndicator')
      [currentTab].classList.add('finish');
  }

  console.log('Form status:', valid);
  return valid;
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i,
    x = document.getElementsByClassName('stepIndicator');
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(' active', '');
  }
  //... and adds the "active" class on the current step:
  x[n].className += ' active';
}
// ------------------------------------
// multi step form handling start
// ------------------------------------

//-------------------
// image upload
//-------------------

function ImgUpload() {
  var imgWrap = $('.upload-img-wrap');

  $('.add-more').click(function (e) {
    console.log('Add More Photos button clicked.');
    e.preventDefault();
    // Trigger file input inside the upload-btn
    $('.upload-btn .upload-inputfile').click();
  });
  var addMoreButton = $('.add-more');

  $('.upload-inputfile').on('change', function (e) {
    $('.upload-btn').addClass('d-none');
    imgWrap.addClass('uploaded');
    addMoreButton.removeClass('d-none');
    imgWrap.removeClass('d-none');

    var maxLength = parseInt($(this).attr('data-max_length'));

    var files = e.target.files;
    var filesArr = Array.prototype.slice.call(files);

    filesArr.forEach(function (f, index) {
      if (!f.type.match('image.*')) {
        return;
      }

      if (imgWrap.find('.upload-img-box').length >= maxLength) {
        return false;
      } else {
        var reader = new FileReader();
        reader.onload = function (e) {
          var img = document.createElement('img');
          img.src = e.target.result;
          img.classList.add('upload-img-box');
          imgWrap.append(img);

          // Append close button to the image container
          var closeButton = $('<div class="upload-img-close">&times;</div>');
          $(img).append(closeButton);

          if (imgWrap.find('.upload-img-box').length === 1) {
            imgWrap.find('.upload-img-box:first-child').addClass('large');
          }
        };
        reader.readAsDataURL(f);
      }
    });
    validateForm();
  });

  $('body').on('click', '.upload-img-close', function (e) {
    $(this).closest('.upload-img-box').remove(); // Remove the closest image container
    if (
      imgWrap.find('.upload-img-box.large').length === 0 &&
      imgWrap.find('.upload-img-box').length > 0
    ) {
      imgWrap.find('.upload-img-box:first-child').addClass('large');
    }
    if (imgWrap.find('.upload-img-box').length === 0) {
      imgWrap.addClass('d-none'); // Hide container if no images are uploaded
      addMoreButton.addClass('d-none'); // Hide "Add More Photos" button if no images are uploaded
      $('.upload-btn').show();
      validateForm();
    }
  });

  // Make the upload image wrap sortable
  $('.upload-img-wrap').sortable({
    items: '.upload-img-box',
    cursor: 'move',
    stop: function (event, ui) {
      $(this).find('.upload-img-box').removeClass('large');
      $(this).find('.upload-img-box:first-child').addClass('large');
      validateForm();
    },
  });
}

//-------------------
// image upload end
//-------------------

//-------------------
// lot preview
//-------------------
function generatePreview() {
  // Get form inputs from previous steps
  const formData = $('#lotForm').serializeArray();
  // Get uploaded images
  const uploadedImages = $('.upload-img-wrap img');

  // Get description textarea value
  const description = tinymce
    .get('lotDescription')
    .getContent({ format: 'text' });

  console.log(description);

  // Clear previous preview details
  $('#previewDetails').empty();

  // Generate summary HTML
  let summaryHTML = `<div class="card mb-3">
        <div class="row no-gutters">
            <div class="col-md-4">`;

  if (uploadedImages.length > 0) {
    summaryHTML += `
    <div class="image-container" style="width: 250px; height: 250px; overflow: hidden;">
    <img src="${uploadedImages[0].src}" style="height: 100%; width: 100%; object-fit: contain" class="card-img" alt="Product Image">
    </div>
    `;
  }

  summaryHTML += `</div>
            <div class="col-md-8">
                <div class="card-body">`;

  formData.forEach((field) => {
    if (field.value.trim() !== '') {
      if (field.name == 'lot_name') {
        summaryHTML += `<h5 class="card-title">${field.value}</h5>`;
      }
    }
  });

  // Include description in the summary if it's not empty
  if (description.trim() !== '') {
    summaryHTML += `<p class="card-text">${description}</p>`;
  }

  summaryHTML += `</div>
        </div>
    </div>
    </div>`;

  summaryHTML += `<div class="card">
        <div class="card-body">
            <h5 class="card-title">Summary</h5>
            <div class="row">`;

  let auctionCostsHTML = '';
  let shippingDetailsHTML = '';

  // Display product details
  formData.forEach((field) => {
    if (field.value.trim() !== '') {
      let label = field.name;

      const labelsMap = {
        starting_price: 'Starting Price',
        buy_it_now_price: 'Buy It Now Price',
        reserve_price: 'Reserve Price',
        package_type: 'Package Type',
        package_weight: 'Weight',
        shipment_cost: 'Shipment Cost',
        carrier_type: 'Carrier Type',
      };

      if (labelsMap[field.name]) {
        label = labelsMap[field.name];
      }

      if (
        field.name == 'starting_price' ||
        field.name == 'buy_it_now_price' ||
        field.name == 'reserve_price'
      ) {
        auctionCostsHTML += `<div class="col-md-12">
                    <p class="text-muted">${label}: ${field.value}</p>
                </div>`;
      }

      if (
        field.name == 'package_type' ||
        field.name == 'package_weight' ||
        field.name == 'shipment_cost' ||
        field.name == 'carrier_type'
      ) {
        shippingDetailsHTML += `<div class="col-md-12">
                    <p class="text-muted">${label}: ${field.value}</p>
                </div>`;
      }
    }
  });

  // Append auction costs and shipping details
  if (auctionCostsHTML !== '') {
    summaryHTML += `<div class="col-md-6">
            <h6 class="font-weight-bold">Auction Costs:</h6>
            <div class="row">
                ${auctionCostsHTML}
            </div>
        </div>`;
  }

  if (shippingDetailsHTML !== '') {
    summaryHTML += `<div class="col-md-6">
            <h6 class="font-weight-bold">Shipping Details:</h6>
            <div class="row">
                ${shippingDetailsHTML}
            </div>
        </div>`;
  }

  summaryHTML += `</div>
        </div>
    </div>`;

  // Append summary to the preview section
  $('#previewDetails').html(summaryHTML);
}
//-------------------
// lot preview end
//-------------------

//-----------------------
// Category search
//-----------------------

// user category search
// Function to fetch categories using AJAX
function fetchCategories(searchValue) {
  var categoriesUrl =
    "{% url 'lots:search_categories' %}" + '?search_query=' + searchValue;
  console.log(categoriesUrl);
  fetch('/search/categories/' + '?search_query=' + searchValue, {
    method: 'GET',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.categories && data.categories.length > 0) {
        console.log(data);
        generateCategoryRadios(data.categories);
      } else {
        document.getElementById('categoryResult').innerHTML =
          '<p>No categories found</p>';
      }
    })
    .catch((error) => console.error('Error:', error));
}

// Event listener for input change
document
  .querySelector('.search-icon input[name="category_search_query"]')
  .addEventListener('input', function () {
    console.log('cat');
    var searchValue = this.value.toLowerCase().trim();
    if (searchValue.length === 0) {
      // Clear category results if search query is empty
      document.getElementById('categoryResult').innerHTML = '';
      return;
    }
    fetchCategories(searchValue);
  });

function generateCategoryRadios(categories) {
  var categoryResultDiv = document.getElementById('categoryResult');
  categoryResultDiv.innerHTML = '';

  categories.forEach(function (category) {
    var radioDiv = document.createElement('div');
    radioDiv.classList.add('form-check', 'flex-column');

    var radioInput = document.createElement('input');
    radioInput.type = 'radio';
    radioInput.name = 'category_type';
    radioInput.id = category.id;
    radioInput.value = category.name;
    radioInput.classList.add('form-check-input');

    var radioLabel = document.createElement('label');
    radioLabel.classList.add('form-check-label');
    radioLabel.htmlFor = category.id;
    radioLabel.textContent = category.name;

    radioDiv.appendChild(radioInput);
    radioDiv.appendChild(radioLabel);

    categoryResultDiv.appendChild(radioDiv);
  });
}

//-----------------------
// Category search END
//-----------------------

function storeImages() {
  const uploadedImages = $('.upload-img-wrap img');
  const imageSrcs = [];
  console.log('store imagages');

  // Collect the src attribute of each uploaded image
  uploadedImages.each(function (index, img) {
    const src = img.src;
    imageSrcs.push(src);
  });

  // Send the image data to the server using AJAX
  $.ajax({
    url: '/lot/images/save/', // Replace '/save_images/' with the URL of your Django view
    method: 'POST',
    data: { images: imageSrcs }, // Send the image srcs as JSON data
    success: function (response) {
      console.log('Images saved successfully:', response);
      // Optionally, do something with the response from the server
    },
    error: function (xhr, status, error) {
      console.error('Error saving images:', error);
    },
  });
}

$('#lotForm').submit(function (event) {
  event.preventDefault(); // Prevent the default form submission
  $(this).unbind('submit').submit();
  storeImages(); // Call the function to store the images
  // Optionally, submit the form after storing the images
});
