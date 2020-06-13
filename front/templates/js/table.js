/*
Scripts for table functionalities.
*/


const _format_cells = function() {
    const cells = document.getElementsByClassName("data-number");

    for(var i = 0; i < cells.length; i++) {
        const cur_value = cells[i].innerHTML;
        if(/^\d+$/.test(cur_value)) {
            var new_value = Number(cur_value).toLocaleString('pt-br');
            cells[i].innerHTML = new_value;
        }
    }
}


const _merge_cells = function(transforms) {
    const cells = document.getElementsByClassName('table_row');

    var elements_to_remove = [];

    for(var i = 0; i < cells.length; i++) {
        const cur_table_row = cells[i].getElementsByClassName('table_small');

        for(var j = 0; j < transforms.length; j++) {
            const transform = transforms[j];
            const receiver_index = transform[0];
            const sender_index = transform[1];

            var receiver = cur_table_row[receiver_index].getElementsByClassName('data-number')[0];
            var sender = cur_table_row[sender_index].getElementsByClassName('data-number')[0];

            if((receiver !== undefined) && (sender !== undefined)) {
                const receiver_content = receiver.innerHTML;
                const sender_content = sender.innerHTML;

                if(sender_content !== '-') {
                    const new_receiver_content = receiver_content + ' (+' + sender_content + ')';
                    receiver.innerHTML = new_receiver_content;
                }
            }

            elements_to_remove.push(sender.parentElement);
        }
    }

    for(var i = 0; i < elements_to_remove.length; i++) {
        const element = elements_to_remove[i];
        element.remove();
    }
}


const table_post_load = function() {
    _format_cells();
    _merge_cells([
        [1, 6],
        [2, 7]
    ]);
}
