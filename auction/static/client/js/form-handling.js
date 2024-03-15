
    // handling user form
    function setupFormAjax(formElement, url, successCallback, errorCallback) {
      formElement.addEventListener("submit", function (e) {
        e.preventDefault();
        const csrftoken = Cookies.get('csrftoken');
        var formData = new FormData(this);

        // Append CSRF token to form data
        formData.append('csrfmiddlewaretoken', csrftoken);

        // send HTTP request
        fetch(url, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': csrftoken
          },
          credentials: 'same-origin', // Send cookies with the request
        })
          .then(response => response.json())
          .then(data => {
            if (data.status === 'ok') {
              console.log("Success");
              if (successCallback) {
                successCallback(data);
              }
            } else {
              if (errorCallback) {
              console.log("error");

                errorCallback(data);
              }
            }
          })
          .catch(error => {
            console.log(url)
            if (errorCallback) {
              errorCallback(error);
            }
          });
      });
    }

    // Function to fetch data from URL and populate form fields using tab
    function fetchDataAndPopulate(url, fieldIds) {
      fetch(url)
        .then(response => {
          console.log(url);
          return response.json()
        })
        .then(data => {
          // Populate form fields with fetched data
          for (const [key, value] of Object.entries(data)) {
            if (fieldIds.hasOwnProperty(key)) {
              document.getElementById(fieldIds[key]).value = value;
            }
          }
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }