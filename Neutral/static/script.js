$(function(){
    $("#calories_error").hide();
    $("#carb_error").hide();
    $("#fat_error").hide();
    $("#sat_error").hide();
    $("#protein_error").hide();
    $("#sodium_error").hide();
    $("#fibres_error").hide();

    var error_calories = false;
    var error_carb = false;
    var error_fat = false;
    var error_sat = false;
    var error_protein = false;
    var error_sodium = false;
    var error_fibres = false;

    $("calories").focusout(function(){
        check_calories();
    });

    $("carb").focusout(function(){
        check_calories();
    });

    $("fat").focusout(function(){
        check_calories();
    });

    $("sat").focusout(function(){
        check_calories();
    });

    $("protein").focusout(function(){
        check_calories();
    });

    $("sodium").focusout(function(){
        check_calories();
    });

    $("fibres").focusout(function(){
        check_calories();
    });
}