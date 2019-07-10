$(document).ready(function () {
    $('input[name="username"]').keyup(function(){
        console.log("something has been typed in username field")
        var data = $(this).serialize()   // capture all the data in the field
        console.log(data)
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/username",
            data: data
        })
        .done(function(res){
            $('.availability').html(res)  // manipulate the dom when the response comes back
        })
    })
})