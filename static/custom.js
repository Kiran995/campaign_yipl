$(document).ready(function() {

    // $('#yes').click(function(){
    //     var currentdate = new Date().toISOString().replace(/\..+/, '') ;
    //     var time = $('#yes').val(currentdate);
    //     console.log(time);
    //     console.log('yes');
    // });
    $('.form-check-input').click(function(e) {
        $(this).next().toggleClass('show-form');

    });

    $('#save').click(function(e) {
        e.preventDefault();
        var currentdate = new Date();
        var time = currentdate.getTime();

        //JavaScript doesn't have a "time period" object, so I'm assuming you get it as a string
        var timePeriod = "05:45:00"; //I assume this is 15 minutes, so the format is HH:MM:SS

        var parts = timePeriod.split(/:/);
        var totaldatetime = (parseInt(parts[0], 10) * 60 * 60 * 1000) + (parseInt(parts[1], 10) * 60 * 1000) + (parseInt(parts[2], 10) * 1000);

        var newDate = new Date();
        var nepalidate = newDate.setTime(time + totaldatetime);
        var formattednepalidate = newDate.toISOString().replace(/\..+/, '');
        console.log(formattednepalidate);

        if($('#time').val()=='Now'){
            var time = $('#yes').val(formattednepalidate);
            console.log(formattednepalidate);
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