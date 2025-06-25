/*Loads the header and footer*/
 
fetch('/header.html')
  .then(res => res.text())
  .then(html => {
    document.getElementById('header').innerHTML = html;

    // Ensure dropotron is initialized AFTER header is inserted
    $('#nav > ul').dropotron({
      offsetY: -22,
      mode: 'fade',
      noOpenerFade: true,
      alignment: 'center'
    });
  });

  fetch('/contact-us.html')
  .then(res => res.text())
  .then(html => {
    document.getElementById('contact-us').innerHTML = html;

    // Ensure dropotron is initialized AFTER header is inserted
    $('#nav > ul').dropotron({
      offsetY: -22,
      mode: 'fade',
      noOpenerFade: true,
      alignment: 'center'
    });
  });
