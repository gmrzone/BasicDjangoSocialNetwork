(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else{
        document.body.appendChild(document.createElement('script')).src='https://saiyedafzal.com:8000/static/js/bookmark.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();

// (function(){
//     if (window.myBookmarklet !== undefined){
//     myBookmarklet();
//     }
//     else {
//     document.body.appendChild(document.createElement('script')).
//    src='https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.
//    floor(Math.random()*99999999999999999999);
//     }
//    })();
// the above script discovers whether the bookmark has already been loaded by checking whether the bookmark variable is defined. by doind so we avoid loading it again if 
// user click on bookmark multiple times if myBookmarklet is not defined you load another javascript file by adding a <script. element to document. the script tag loads the \
// bookmark.js located in static folder. we are using randem number as perameter for js file because we dont want to load the script from browser cache memory. the actual 
// bookmark code is located in bookmark.js static file. This file allow to update bookmark code without requiring user to update the bookmark they previously added to browser
