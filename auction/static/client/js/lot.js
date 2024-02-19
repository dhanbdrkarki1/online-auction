// shows bids made by bidder
document.getElementById('seeAllBids').addEventListener('click', function () {
  var bids = document.getElementsByClassName('user-bid');
  var icon = this.getElementsByTagName('i')[0];

  for (var i = 0; i < bids.length; i++) {
    if (bids[i].style.display === 'none') {
      bids[i].style.display = 'flex';
      icon.classList.remove('bi-chevron-down');
      icon.classList.add('bi-chevron-up');
      this.innerHTML = "Hide bids(5) <i class='bi bi-chevron-up'></i>";
    } else {
      bids[i].style.display = 'none';
      icon.classList.remove('bi-chevron-up');
      icon.classList.add('bi-chevron-down');
      this.innerHTML = "See all bids(5) <i class='bi bi-chevron-down'></i>";
    }
  }
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
