function get_request( url, response_handler, error_handler ) {
    fetch( url )
        .then((resp) => resp.json())
        .then( response_handler ) // Handle data from GET request
        .catch( error_handler ); //Error handler must take in single variable
}

function post_request( url, data, post_response_function ) {
    fetch( url, { body: JSON.stringify( data ),
                  method: "POST",
                  headers: { "Content-Type": "application/json" } 
                } )
        .then( post_response_function );
}

function post_null_response() {
    // Do nothing with server response
}

function get_default_error_handler( error ) {
    console.error(error);
}
