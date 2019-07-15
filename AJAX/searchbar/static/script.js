$(document).ready(function () {
    $('input[name="username"]').keyup(function(){
        console.log("something has been typed in username field")
        var data = $(this).serialize() 
        console.log(data)
        $.ajax({
            method: "POST",   
            url: "/username",
            data: data
        })
        .done(function(res){
            $('.availability').html(res)
        })
    })

    $('input[name="name"]').keyup(function () {
        console.log("something has been typed in username field")
        var data = $(this).serialize()    // capture all the data in the field
        console.log(data)
        $.ajax({
            method: "GET",  // we are using a get request here, but this could also be done with a post
            url: "/usersearch",
            data: data
        })
        .done(function(res){
            $('.results').html(res)   // manipulate the dom when the response comes back
        })
    })
})