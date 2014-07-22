$(function() {
    function getCookie(name)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
 
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
 
    $.ajaxSetup({ 
        crossDomain: false, // obviates need for sameOrigin test
         beforeSend: function(xhr, settings) {
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
            
                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
             }
         } 
    });
    
    var SelectAction = function() {
        
    };
    
    SelectAction.prototype = {
        initialize: function() {
            var that = this;
            that.albumList = new AlbumList(that);
            that.albumList.add(0, '(NONE)');
            that.albumList.add_divider();
            that.albumList.request(function(albums) {
                that.albumList.update(albums);    
                that.albumView(0);
            });
        },
        
        albumView: function(idx) {
            this.albumList.view(idx)
        },
        
        onAlbumChanging: function(album) {
            console.log(album);
        },
    };
    
    var action = new SelectAction();
    action.onAlbumChanging = function(album) {
        $("#id_album").attr("value", album.id);
    }
    

    action.initialize();


});