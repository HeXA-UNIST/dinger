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

    function request_photos(aid, next, callback) {
        $.ajax({
            type: "POST",
            url: "photos",
            dataType: "json",
            data: {"album": aid, "next": next}
            
        }).done(function(data){
            if (data.status == 0)
                callback(data.result);
        });
    }
    

    var PHOTO_PER_ROW = 4
    
    // var albumListNode = $("#album_list");
    var albumPageNode = $("#album_page");
    
    /* var AlbumList = function(listener) {
        this.albums = [];
        this.listener = listener;
        this.list_node = albumListNode.find('ul');  
            
        this.add(0, '(ALL)');
        this.add_divider();
    }
    
    AlbumList.prototype = {
       
        view: function(idx) {
            if (0 > idx) return;
            if (idx >= this.albums.length) return;
            
           
            
            this.listener.onAlbumChanging(this.albums[idx]);            
        }, 
         
        add: function(album_id, name) {
            var that = this;
            
            var node = $("<li>");
            var link = $("<a>");
            var idx = that.albums.length;
            
            link.attr("role", "menuitem").attr("tabindex","-1").attr("href","#");
            link.append(name);
            node.append(link);
             
            link.on("click", function(e) {
                that.listener.albumView(idx);
                return true;
            });
            
            that.albums.push({id: album_id, name: name});
            this.list_node.append(node);
        },
        
        add_divider: function() {
            var divider = $("<li>").attr("class", "divider");
            this.list_node.append(divider);
        },
        
        
        update: function(albums) {
            var len = albums.length;
            for (var i=0; i<len; i++) {
                this.add(albums[i].id, albums[i].name);
            }
        }
             
    };
    */
    
    var Album = function(page, album_id) {
        
        this.page = page;
        this.album = album_id;
        this.photos = new Array();
        
        this.albumRows = [];
        this.currentPhoto = 0;
        this.size = 0;
        this.leftSize = -1;
        this.node = $("<div>");
        
        albumPageNode.append(this.node);
    };
    
    Album.prototype = {
        complete: function() {
            return this.leftSize == 0;
        }, 
        request: function(callback) {
            var that = this;
            request_photos(this.album,
                this.currentPhoto,
                function(data) {
                    if (that.currentPhoto != 0 && that.currentPhoto <= data.next)
                     return;
                    var length = data.size;
                    for (var i=0; i<length; i++) {
                        that.add(data.photos[i])
                    }
                    that.currentPhoto = data.next;
                    that.size += length;
                    that.leftSize = data.left_size;
                    callback();
                });
        },
        
        add: function(photo) {
            var that = this;
            var length = that.photos.length;        
            if (length % PHOTO_PER_ROW > 0) {
                var row = that.albumRows.pop();
            } else {
                // insert a row.
                
                var stand = $("<div>").attr("class", "row");
                var details = $("<div>").attr("class", "photo_details")
                                .append($("<img>"));
                var levelNode = $("<div>")
                                .append(stand)
                                .append(details);
                that.node.append(levelNode);
                
                var row = {stand: stand,
                            details: details
                            }
            }
            
            var node = $("<div>").attr("class", "col-md-3")
                        .append($("<a>").attr("class", "thumbnail")
                            .append($("<img>").attr("src", photo.t_url))
                        );
            row.stand.append(node);    
            that.albumRows.push(row);
            
            var p = {
                photo: photo,
                node: node,
                row: row
            }
            that.photos.push(p);
            node.click(function(){
                that.page.onClickPhoto(p);
            });    
        },
        
        clean: function() {
            this.node.remove();
        }     
    };
    
    var AlbumPage = function() {
        
    };
    
    AlbumPage.prototype = {
        initialize: function() {
            var that = this;
            that.albumList = new AlbumList(that);
            that.albumList.add(0, '(ALL)');
            that.albumList.add_divider();
        
            that.currentAlbumIdx = -1;
            that.currentAlbum = null;
            that.currentPhoto = null;
            
            that.albumList.request(function(albums) {
                that.albumList.update(albums);    
                that.albumView(0);
            });
        },
        
        albumView: function(idx) {
            if (this.currentAlbumIdx != idx) {
                this.albumList.view(idx)
                this.currentAlbumIdx = idx;
            }
        },
        
        onAlbumChanging: function(album) {
        },
        
        onClickPhoto: function(photo) {
        },
        
        onScroll: function() {
        }
    };
    
    var page = new AlbumPage();
    page.onAlbumChanging = function(album) {
        var that = this;
        
        if (that.currentAlbumIdx != -1)
            that.currentAlbum.clean();
        var alb  = new Album(that, album.id);
        alb.request(function() {
            
        });
        console.log(this.albumList);
        that.currentAlbum = alb;
    }
    
    page.onClickPhoto = function(photo) {
        if (this.currentPhoto == photo) {
            photo.row.details.slideUp();
            this.currentPhoto = null;
        } else {
            var detailNode = photo.row.details;
            detailNode.find("img").attr("src", photo.photo.url);
                
            if (this.currentPhoto == null || this.currentPhoto.row != photo.row) {
                if (this.currentPhoto != null)
                    this.currentPhoto.row.details.slideUp("fast");
                photo.row.details.slideDown(function() {
                    $('html,body').animate({scrollTop: photo.row.details.position().top-140 }, "fast");
                });
            }
            this.currentPhoto = photo;   
        }
    }
    
    page.onScroll = function(e) {
        if (this.currentAlbum.complete()) return;
        var contentHeight = albumPageNode.height();
        var contentTop = albumPageNode.position().top;
        var pageHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        
        console.log(contentHeight - pageHeight + contentTop - scrollTop);
        
        if (contentHeight - pageHeight + contentTop - scrollTop < 220) {
            this.currentAlbum.request(function() {});
        }
    }
    
    page.initialize();

    $(window).scroll(function(e) {
        page.onScroll()
    });
    
});
