function showMessage(alertClass, message) {
  var notification = $("#notification");
  notification.find(".alert")
              .removeClass(["alert-success", "alert-danger"])
              .find(".message").text(message).end()
              .find(".status").text(alertClass === "alert-success" ? "Success!" : "Error:").end()
              .addClass(alertClass).removeClass("hide");
  notification.modal("show");
}

function toggleProp(el, propName) {
  el.prop(propName, !el.prop(propName));
}

function saveComment(reload) {
  $.ajax({
    url: this.attr("action"),
    data: this.serialize(),
    context: this,
    type: this.attr("method"),
    success: function (response) {
      var data = JSON.parse(response);
      showMessage("alert-success", data.message);
      if(reload) {
        setTimeout(function () {
          location.reload();
        }, 3000);
      }
    },
    error: function (data) {
      showMessage("alert-danger", data.responseText);
    }
  });
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
  saveComment.apply($(this), [true]);
});

$(".comment-header").on("click", ".comment-btn", function () {
  var el = $(this);
  var textArea = el.closest("form").find("textarea");

  if(el.hasClass("edit")) {
    textArea.data("original-value", textArea.val());
  } else if (el.hasClass("cancel")) {
    textArea.val(textArea.data("original-value"));
  } else if (el.hasClass("confirm")) {
    saveComment.apply(el.closest("form"));
  }

  //toggle edit and confirm buttons visibilty
  el.parent().find("span").toggleClass("hide");
  //add/remove readonly to textArea
  toggleProp(textArea, "readonly");
});
