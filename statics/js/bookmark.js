(function(){
    var jquery_version = '3.5.1';
    var site_url = 'https://saiyedafzal.com:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;
    function myBookmarklet(mssg){
        //  load css
        // create a link tag
        var css = jQuery('<link>');
        // add arrtibute to link tag
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url+'css/bookmarklet.css?r='+Math.floor(Math.random()*99999999999999999999),
        });
        // append link tag to head
        jQuery('head').append(css);

        // load HTML
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Please Select a image To Bookmark it..</h1><div class="images"></div></div>';
        jQuery('body').append(box_html)

        // close event
        jQuery('#bookmarklet #close').click(function(){
            jQuery('#bookmarklet').remove();
        });

        //find images and Add Image to htmlBox div tag
        jQuery.each(jQuery('img[src$="jpg"]'),function(index, image){
            image_url = jQuery(image).attr('src');
            if(jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
                jQuery('#bookmarklet .images').append('<a href="#"><img ' + 'src="'+image_url+'" /></a>');
            }
        });

        // add event listner to image click to open new window to create a post
        jQuery('#bookmarklet .images a').click(function(){
            // hide bookmarklet
            jQuery('#bookmarklet').hide()
            // open new window to submit the image
            image_url = jQuery(this).children('img').attr('src');
            https://127.0.0.1:8000/create-image-post/?title=%20Django%20and%20Duke&url=https://wallpapercave.com/wp/T4xxWSN.jpg&description=afzal%20saiyed.
            window.open(site_url+'create-image-post/?url='+encodeURIComponent(image_url)+'&title='+encodeURIComponent(jQuery('title').text()),'_blank');
        })

    };
    // id window.jQuery is not undefined run myBookmarklet function
    if(typeof(window.jQuery) != 'undefined'){
        myBookmarklet()
    }
    else{
        // check for conflicts
        var conflict = typeof(window.$) != 'undefined';
        // create a script tag
        var script = document.createElement('script');
        // add script tag attribute src to jquery cdn link
        script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/'+jquery_version+'/jquery.min.js';
        // append the script tag to document head
        document.head.appendChild(script);
        //  create a way to wait until script loading
        var attempt = 15;

        (function(){
            // check again if jquery is undefined
            if(typeof(window.jQuery) == 'undefined'){
                if(--attempt > 0){
                    window.setTimeout(arguments.callee, 250)
                }
                else{
                    alert('An Error Occured While Loading Jquery')
                }
            }
            else{
                myBookmarklet()
            }

        })()

    }

})();