$(document).ready(function() {

    // $('#yes').click(function(){
    //     var currentdate = new Date().toISOString().replace(/\..+/, '') ;
    //     var time = $('#yes').val(currentdate);
    //     console.log(time);
    //     console.log('yes');
    // });
    //
    // $('#no').click(function(e) {
    //     e.preventDefault();
    //     var schedule = $('#time').val();
    //     var notime = $('#no').val(schedule);
    //     console.log(notime);
    //     console.log('no');
    //
    // });

    $('#save').click(function(e) {
        e.preventDefault();
        var currentdate = new Date().toISOString().replace(/\..+/, '');
        console.log(currentdate);

        if($('#time').val()=='Now'){
            var currentdate = new Date().toISOString().replace(/\..+/, '');
            console.log(currentdate);
            var time = $('#yes').val(currentdate);
        }else{
            var notime = $('#no').val($('#time').val());
            console.log('******')
            console.log(notime)
        }
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