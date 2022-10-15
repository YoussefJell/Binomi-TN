$(document).ready(function () {
  // look for places_search
  let dict = {};
  $.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5001/api/v1/users_search/',
    data: JSON.stringify(dict),
    success: function (result) {
      for (let i in result) {
        let users_content = [
          '<div class="card card--fixedWidth">',
          '<div class="Price">',
          '<button class="cardProfileBtn" onclick="window.location.href=\'/profile?=' + result[i].id + '\'"></button>',
          '<h6>' + result[i].first_name + ' ' + result[i].last_name + '</h6>',
          '</div>',
          '<div class="cardDescription">',
          '<p>' + result[i].description + '</p>',
          '</div>',
          '<div class="cardLocation">',
          '<p>Location: ' + result[i].location_id + '</p>',
          '</div>',
          '</div>'
        ];
        $(users_content.join('')).appendTo('div.cards-wrapper');
      }
    },
    dataType: 'json',
    contentType: 'application/json'
  });

  // look for api_status
  //$.get('http://0.0.0.0:5001/api/v1/status/', function (data) {
  //  if (data['status'] === 'OK') {
  //    $('DIV#api_status').addClass('available');
  //  } else {
  //    $('DIV#api_status').removeClass('available');
  //  }
  //});

  let my_dict = {};

  $('input[type=checkbox]').click(function () {

    if ($(this).is(':checked')) {
      my_dict[$(this).data('id')] = $(this).data('name');
      $('.searchTerm h5').text(Object.values(my_dict).join(', '));
    } else if ($(this).not(':checked')) {
      delete my_dict[$(this).data('id')];
      $('.searchTerm h5').text(Object.values(my_dict).join(', '));
      if (Object.getOwnPropertyNames(my_dict).length === 0)
        $('.searchTerm h5').text("Location");
    }
  });



  $("button").click(function () {
    const locationsIds = {
      locations: Object.keys(my_dict)
    };
    $('div.cards-wrapper').empty();
    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:5001/api/v1/users_search/',
      data: JSON.stringify(locationsIds),
      success: function (result) {
        for (let i in result) {
          let users_content = [
            '<div class="card card--fixedWidth">',
            '<div class="Price">',
            '<button class="cardProfileBtn" onclick="window.location.href=\'/profile?=' + result[i].id + '\'"></button>',
            '<h6>' + result[i].first_name + '</h6>',
            '</div>',
            '<div class="cardDescription">',
            '<p>' + result[i].description + '</p>',
            '</div>',
            '<div class="cardLocation">',
            '<p>Location: ' + result[i].location_id + '</p>',
            '</div>',
            '</div>'
          ];
          $(users_content.join('')).appendTo('div.cards-wrapper');
        }
      },
      dataType: 'json',
      contentType: 'application/json'
    });
  });
});
