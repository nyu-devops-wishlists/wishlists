$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_name").val(res.name);
        $("#wishlist_customer_email").val(res.email);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_name").val("");
        $("#wishlist_customer_email").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#wishlist_name").val();
        var customer_email = $("#wishlist_customer_email").val();

        var data = {
            "name": name,
            "email": customer_email,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();
        var name = $("#wishlist_name").val();
        var customer_email = $("#wishlist_customer_email").val();

        var data = {
            "name": name,
            "email": customer_email,
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/wishlists/" + wishlist_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists/" + wishlist_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/wishlists/" + wishlist_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#wishlist_name").val();
        var customer_email = $("#wishlist_customer_email").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (customer_email) {
            if (queryString.length > 0) {
                queryString += '&email=' + customer_email
            } else {
                queryString += 'email=' + customer_email
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:70%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">CustomerEmail</th>'
            $("#search_results").append(header);
            var firstWishlist = "";
            for(var i = 0; i < res.length; i++) {
                var wishlist = res[i];
                var row = "<tr><td>"+wishlist.id+"</td><td>"+wishlist.name+"</td><td>"+wishlist.email+"</td><td>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstWishlist != "") {
                update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Count Wishlist by Customer
    // ****************************************

    $("#count-btn").click(function () {

        var customer_email = $("#wishlist_customer_email").val();

        var queryString = ""

        if (customer_email) {
            if (queryString.length > 0) {
                queryString += '&customer_email=' + customer_email
            } else {
                queryString += 'customer_email=' + customer_email
            }
        } 

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            var count = 0;
            for(var i = 0; i < res.length; i++) {
                count++
            }

            flash_message("Customer_email " + customer_email + " has " + count + " wishlists " )
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });
})

