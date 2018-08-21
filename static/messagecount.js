    $(document).ready(function(){
            function hasUnicode(str) {
                for (var i = 0, n = str.length; i < n; i++) {
                    if (str.charCodeAt( i ) > 255) { return true; }
                }
                return false;
            }

            // unescape(encodeURIComponent('जास')).length

            $('#message').keyup(function(){
                var message = $(this).val();
                var chars = message.length;

                // for (var i = 0, n = str.length; i < n; i++) {
                //     console.log(st)
                    if (hasUnicode(message)) {
                        part1Count = 70;
                        part2Count = 64;
                        part3Count = 67;
                        console.log(chars);
                    }else {
                        part1Count = 160;
                        part2Count = 146;
                        part3Count = 153;
                        console.log(chars);
                    }
                messages = 0;
                remaining = 0;
                total = 0;
                if (chars <= part1Count) {
                    messages = 1;
                    remaining = part1Count - chars;
                } else if (chars <= (part1Count + part2Count)) {
                    messages = 2;
                    remaining = part1Count + part2Count - chars;
                } else if (chars > (part1Count + part2Count)) {
                    moreM = Math.ceil((chars - part1Count - part2Count) / part3Count) ;
                    console.log('Apple');
                    console.log(moreM);
                    remaining = part1Count + part2Count + (moreM * part3Count) - chars;
                    messages = 2 + moreM;
                }
                // }


            $('#remaining').text(remaining);
            $('#messages').text(messages);
            $('#total').text(chars);
            if (remaining > 1) $('.cplural').show();
                else $('.cplural').hide();
            if (messages > 1) $('.mplural').show();
                else $('.mplural').hide();
            if (chars > 1) $('.tplural').show();
                else $('.tplural').hide();
        });
            $('#message').keyup();
        });
