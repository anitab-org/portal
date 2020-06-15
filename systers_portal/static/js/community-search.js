const input = $("#form1")
const result_div = $('#cards')
const endpoint = '/community/search'
const delay_by_in_ms =300
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            result_div.fadeTo('fast', 0).promise().then(() => {
                result_div.html(response['html'])
                result_div.fadeTo('fast', 1)

            })
        })
}
input.on('keyup', function () {

    const request_parameters = {
        query: $(this).val()
    }
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
