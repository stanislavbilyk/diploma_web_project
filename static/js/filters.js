
$(document).ready(function () {
    $(".Filter_header").click(function () {
        $(this).next(".Filter_options").slideToggle();
        $(this).toggleClass("active");
    });

    $("#price_range").on("input", function () {
        let min = $("#price_range").attr("min");
        let max = $(this).val();
        $("#price_value").text(min + " - " + max);
        $("#price_min").val(min);
        $("#price_max").val(max);
    });

    $(".Filter_options input").on("change", function () {
        $("#Filter_form").submit();
    });
    $(".Filter_options input[name='built_in_memory']").on("change", function () {
    $("#Filter_form").submit();
});
    $(".Filter_options input[name='camera']").on("change", function () {
    $("#Filter_form").submit();
});
    $(".Filter_options input[name='ram']").on("change", function () {
    $("#Filter_form").submit();
});
});





