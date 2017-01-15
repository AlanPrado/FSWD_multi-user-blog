function showMessage(alertClass, message) {
  var notification = $("#notification");
  notification.find(".alert")
              .removeClass(["alert-success", "alert-danger"])
              .find(".message").text(message).end()
              .find(".status").text(alertClass === "alert-success" ? "Success!" : "Error:").end()
              .addClass(alertClass).removeClass("hide");
  notification.modal("show");
}

$("#delete-post").on("submit", "form", function (ev) {
    ev.preventDefault();
    var modal = $(this);
    var $btn = modal.find("button").button('loading');
    var post_id = modal.find("input[name=post_id]").val();

    $.ajax({
      url: '/blog/' + post_id,
      type: 'DELETE',
      success: function (response) {
        var data = JSON.parse(response);
        showMessage("alert-success", data.message);
        $(".detail").remove();
      },
      error: function (data) {
        showMessage("alert-danger", data.responseText);
      },
      complete: function () {
        modal.closest("#delete-post").modal("hide");
        $btn.button("reset");
      }
    });
});

$(".post-detail").on("click", ".like", function () {
  var el = $(this);
  var url = el.data("url");

  $.ajax({
    url: url,
    type: 'POST',
    success: function (response) {
      el.toggleClass("active");
    },
    error: function (data) {
      showMessage("alert-danger", data.responseText);
    }
  });
});
