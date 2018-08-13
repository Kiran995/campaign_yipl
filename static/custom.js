$(document).ready(function() {

    $('#save').click(function(e) {
        e.preventDefault();


        Papa.parse($('#file')[0].files[0],{
            skipEmptyLines: true,
            header:true,
            complete:function(results){
                csv_data = JSON.stringify(results.data);
                $('#hidden').val(csv_data);
                $.ajax({
                    url: 'valid',
                    data: {data: csv_data},
                    type: 'POST',
                    dataType: 'json',
                    success: function(data) {
                        if(confirm(data.valid_count + ' valid phone numbers ' + data.invalid_count + ' invalid phone numbers. Do you want to proceed? ')){
                            alert('Proceed anyway');
                            $('#add-campaign-form').submit();
                        }else{
                            alert('No')
                        }
                    },
                    error: function(data) {

                    }
                });
            }
        });


    });
});