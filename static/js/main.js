/*
dropdown menu functionality
*/
$(function () {
  $('#nav > ul').dropotron({
    offsetY: -22,
    mode: 'fade',
    noOpenerFade: true,
    alignment: 'center'
  });
});
window.addEventListener('load', () => {
  document.body.classList.add('loaded');
  document.body.classList.remove('is-preload');
});


/*Show more button functionality*/
document.addEventListener('DOMContentLoaded', function () {
  const showMoreButton = document.getElementById('show-more');

  showMoreButton.addEventListener('click', function (event) {
    event.preventDefault();

    const hiddenArticles = document.querySelectorAll('.article.hidden');
    const batch = Array.from(hiddenArticles).slice(0, 3); // show 3 at a time

    batch.forEach((article) => {
      requestAnimationFrame(() => {
        article.classList.remove('hidden');
      });
    });

    if (hiddenArticles.length <= 3) {
      showMoreButton.style.display = 'none';
    }
  });
});

$(
  '<div id="titleBar">' +
    '<a href="#navPanel" class="toggle"></a>' +
  '</div>'
).appendTo($body);

$(
  '<div id="navPanel">' +
    '<nav>' + $('#nav').navList() + '</nav>' +
  '</div>'
).appendTo($body)
.panel({
  delay: 500,
  hideOnClick: true,
  hideOnSwipe: true,
  resetScroll: true,
  resetForms: true,
  side: 'left',
  target: $body,
  visibleClass: 'navPanel-visible'
});







(function($) {

	var	$window = $(window),
		$body = $('body');

	// Breakpoints.
		breakpoints({
			xlarge:  [ '1281px',  '1680px' ],
			large:   [ '981px',   '1280px' ],
			medium:  [ '737px',   '980px'  ],
			small:   [ null,      '736px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Dropdowns.
		$('#nav > ul').dropotron({
			mode: 'fade',
			noOpenerFade: true,
			hoverDelay: 150,
			hideDelay: 350
		});

	// Nav.

		// Title Bar.
			$(
				'<div id="titleBar">' +
					'<a href="#navPanel" class="toggle"></a>' +
				'</div>'
			)
				.appendTo($body);

		// Panel.
			$(
				'<div id="navPanel">' +
					'<nav>' +
						$('#nav').navList() +
					'</nav>' +
				'</div>'
			)
				.appendTo($body)
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'navPanel-visible'
				});

})(jQuery);
