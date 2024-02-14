$(document).ready(function () {
  console.log('jQuery loaded successfully.');

  ImgUpload();
});

var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  var x = document.getElementsByClassName('step');
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
  var x, y, i;
  var valid = true;
  x = document.getElementsByClassName('step');
  y = x[currentTab].getElementsByTagName('input');
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty and not of type file...
    if (y[i].value.trim() === '' && y[i].type !== 'file') {
      // Add an "invalid" class to the field:
      y[i].classList.add('invalid');
      // Set the current valid status to false:
      valid = false;
    }
  }
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

// image upload

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
    $('.upload-btn').hide();
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

    // Clear file input
    $(this).val('');
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

function generatePreview() {
  // Get form inputs from previous steps
  const formData = $('#lotForm').serializeArray();
  // Get uploaded images
  const uploadedImages = $('.upload-img-wrap img');

  // Clear previous preview details
  $('#previewDetails').empty();

  // Generate summary HTML
  let summaryHTML = '<h4>Preview:</h4>';

  // Display first uploaded image
  if (uploadedImages.length > 0) {
    summaryHTML += `<div class="product-image"><img src="${uploadedImages[0].src}" alt="Product Image"></div>`;
  }

  // Display product details
  summaryHTML += '<div class="product-details">';
  formData.forEach((field) => {
    if (field.value.trim() !== '') {
      summaryHTML += `<p><strong>${field.name}:</strong> ${field.value}</p>`;
    }
  });
  summaryHTML += '</div>';

  // Display auction costs
  summaryHTML += '<div class="auction-cost">';
  summaryHTML += '<h5>Auction Costs:</h5>';
  // Include VAT, Commission, Overall Cost logic here
  summaryHTML += '</div>';

  // Display shipping details
  summaryHTML += '<div class="shipping-details">';
  summaryHTML += '<h5>Shipping Details:</h5>';
  // Include shipping details logic here
  summaryHTML += '</div>';

  // Display bidding starting date
  summaryHTML += '<div class="bidding-start-date">';
  summaryHTML += '<h5>Bidding Starting Date:</h5>';
  // Include bidding starting date logic here
  summaryHTML += '</div>';

  // Append summary to the preview section
  $('#previewDetails').html(summaryHTML);
}

//-----------------------
// Category search
//-----------------------

// user category search
// Function to fetch categories using AJAX
function fetchCategories(searchValue) {
  var categoriesUrl =
    "{% url 'lots:search_categories' %}" + '?search_query=' + searchValue;
  console.log(categoriesUrl);
  fetch('/seller/search-categories/' + '?search_query=' + searchValue, {
    method: 'GET',
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.categories && data.categories.length > 0) {
        generateCategoryRadios(data.categories);
        console.log(data);
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

// generate radio buttons for categories
function generateCategoryRadios(categories) {
  var categoryResultDiv = document.getElementById('categoryResult');
  categoryResultDiv.innerHTML = ''; // Clear previous results

  categories.forEach(function (category) {
    var radioDiv = document.createElement('div');
    radioDiv.classList.add('form-check', 'flex-column'); // Added 'flex-column' class

    var radioInput = document.createElement('input');
    radioInput.type = 'radio';
    radioInput.name = 'categoryResult';
    radioInput.id = category.toLowerCase();
    radioInput.value = category;
    radioInput.classList.add('form-check-input');

    var radioLabel = document.createElement('label');
    radioLabel.classList.add('form-check-label');
    radioLabel.htmlFor = category.toLowerCase();
    radioLabel.textContent = category;

    radioDiv.appendChild(radioInput);
    radioDiv.appendChild(radioLabel);

    categoryResultDiv.appendChild(radioDiv);
  });
}

//-----------------------
// Category search END
//-----------------------
