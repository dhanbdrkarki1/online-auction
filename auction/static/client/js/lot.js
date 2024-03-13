// web socket for lot detail page
document.addEventListener('DOMContentLoaded', function (event) {
  console.log('lot socket init');
  let location = window.location;
  let wsStart = 'ws://';

  if (location.protocol === 'https:') {
    wsStart = 'wss://';
  }

  var currentLotUrl = location.href;
  var urlParts = currentLotUrl.split('/');
  var lotSlug = urlParts[urlParts.length - 2];
  console.log(lotSlug);

  const urlLot = wsStart + location.host + `/ws/lots/` + lotSlug + '/';

  const requestUser = JSON.parse(
    document.getElementById('request-user').textContent
  );

  const lotSocket = new WebSocket(urlLot);

  lotSocket.onopen = function (e) {
    console.log('WebSocket connection established:', e);
  };

  lotSocket.onmessage = function (e) {
    console.log('Message received from server:', e.data);
    const bidData = JSON.parse(e.data);
    console.log(bidData);

    const latestBids = bidData.latest_bids;
    updateBids(latestBids);
  };

  lotSocket.onerror = function (error) {
    console.error('WebSocket error:', error);
  };

  lotSocket.onclose = function (event) {
    console.error('WebSocket connection closed unexpectedly:', event);
  };
});

// image thumnail for lot detail page
let thumbnails = document.getElementsByClassName('thumbnail');
let activeImages = document.getElementsByClassName('active');

for (var i = 0; i < thumbnails.length; i++) {
  thumbnails[i].addEventListener('mouseover', function () {
    if (activeImages.length > 0) {
      activeImages[0].classList.remove('active');
    }
    this.classList.add('active');
    document.getElementById('featured').src = this.src;
  });
}
let buttonRight = document.getElementById('slideRight');
let buttonLeft = document.getElementById('slideLeft');
buttonLeft.addEventListener('click', function () {
  document.getElementById('slider').scrollLeft -= 160;
});
buttonRight.addEventListener('click', function () {
  document.getElementById('slider').scrollLeft += 160;
});
