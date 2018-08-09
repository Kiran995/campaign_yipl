$(document).ready(function() {

    $('#save').click(function(e) {
        e.preventDefault();

        Papa.parse($('#file')[0].files[0],{
            skipEmptyLines: true,
            header:true,
            complete:function(results){
                csv_data = JSON.stringify(results.data);
                console.log(csv_data);
                $('#hidden').val(csv_data);

                $('#add-campaign-form').submit();
            }
        });
    });
});