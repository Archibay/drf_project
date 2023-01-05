$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-contact-us .modal-content").html("");
        $("#modal-contact-us").modal("show");
      },
      success: function (data) {
        $("#modal-contact-us .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-contact-us .modal-content").html(data.html_contact_us_success);
//          $("#book-table tbody").html(data.html_contact_us);
//          $("#modal-contact-us").modal("hide");
        }
        else {
          $("#modal-contact-us .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  $(".js-contact-us").click(loadForm);
  $("#modal-contact-us").on("submit", ".js-contact-us-form", saveForm);


});
