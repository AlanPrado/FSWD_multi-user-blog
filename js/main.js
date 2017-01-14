$("#delete-post").on("submit", "form", function (ev) {
    ev.preventDefault();
    var modal = $(this);
    var $btn = modal.find("button").button('loading');
    var blog_id = modal.find("input[name=blog_id]").val();
    function showMessage(alertClass, message) {
      $("#alert").removeClass(["alert-success", "alert-danger"])
                 .find(".message").text(message).end()
                 .find(".status").text(alertClass === "alert-success" ? "Success!" : "Error:").end()
                 .addClass(alertClass).removeClass("hide");
    }

    $.ajax({
      url: '/blog/' + blog_id,
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
