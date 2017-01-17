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
      var likes = JSON.parse(response).message;
      el.parent().find(".like_counter span").text(likes);
    },
    error: function (data) {
      showMessage("alert-danger", data.responseText);
    }
  });
});

$("#add-comment").on("submit", "form", function (evt) {
  evt.preventDefault();
  $.ajax({
    url: $(this).attr("action"),
    data: $(this).serialize(),
    context: this,
    type: $(this).attr("method"),
    success: function (response) {
      var data = JSON.parse(response);
      //$(this).find("[name=content]").val("");
      showMessage("alert-success", data.message);
      setTimeout(function () {
        location.reload();
      }, 3000);
    },
    error: function (data) {
      showMessage("alert-danger", data.responseText);
    }
  });
});
