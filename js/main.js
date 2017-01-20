function showMessage(alertClass, message) {
  var notification = $("#notification");
  notification.find(".alert")
              .removeClass("alert-success alert-danger")
              .find(".message").text(message).end()
              .find(".status").text(alertClass === "alert-success" ? "Success!" : "Error:").end()
              .addClass(alertClass).removeClass("hide");
  notification.modal("show");
}

function reload() {
  setTimeout(function () {
    location.reload();
  }, 3000);
}

function editComment(form) {
  request(form.attr("action"), "PUT", form.serialize())
  .fail(function () {
    cancelEditComment(form.find("textarea"));
  });
}

function removeComment(form) {
  request(form.attr("action"), "DELETE")
        .then(function () {
          form.remove();
          reload();
        })
        .fail(function () {
          cancelEditComment(form.find("textarea"));
        });
}

function toggleProp(el, propName) {
  el.prop(propName, !el.prop(propName));
}

function cancelEditComment(textArea) {
  textArea.val(textArea.data("original-value"));
}

//TODO: consider using options
function request(url, method, data, hideSM, hideEM) {
  var defer = $.Deferred();

  $.ajax({
    url: url,
    data: data,
    type: method,
    success: function (response) {
      var data = JSON.parse(response);
      defer.resolve(data);
      if(!hideSM) showMessage("alert-success", data.message);
    },
    error: function (data) {
      defer.reject(data);
      if(!hideEM) showMessage("alert-danger", data.responseText);
    }
  });

  return defer;
}

$("#delete-post").on("submit", "form", function (ev) {
    ev.preventDefault();
    var modal = $(this);
    var $btn = modal.find("button").button('loading');
    var post_id = modal.find("input[name=post_id]").val();

    request('/blog/' + post_id, "DELETE")
    .then(function (data) {
      showMessage("alert-success", data.message);
      $(".detail").remove();
    })
    .done(function () {
      modal.closest("#delete-post").modal("hide");
      $btn.button("reset");
    });
});

$(".post-detail").on("click", ".like", function () {
  var self = $(this);
  var url = self.data("url");

  request(url, "POST", "", true).then(function (data) {
    self.parent().find(".like_counter span").text(data.message);
    self.toggleClass("active");
  });
});

$("#add-comment").on("submit", "form", function (evt) {
  evt.preventDefault();
  var self = $(this);
  request(self.attr("action"), "POST", self.serialize())
    .then(reload);
});

$(".comment-header").on("click", ".comment-btn", function () {
  var el = $(this);
  var textArea = el.closest("form").find("textarea");

  var isEdit = el.hasClass("edit");
  var isRemove = el.hasClass("remove");

  if(isEdit || isRemove) {
    textArea.data("original-value", textArea.val());
    textArea.data("edit", isEdit);
    textArea.data("remove", isRemove);
  } else if (el.hasClass("cancel")) {
    cancelEditComment(textArea);
  } else if (el.hasClass("confirm")) {
    var form = el.closest("form");
    if(textArea.data("edit")) {
      editComment(form);
    } else if(textArea.data("remove")) {
      removeComment(form);
    }
  }

  //toggle edit and confirm buttons visibilty
  el.parent().find("span").toggleClass("hide");
  //add/remove readonly to textArea
  if(!textArea.data("remove"))
    toggleProp(textArea, "readonly");
});
