$(function() {
    function request_albums(callback) {
        $.ajax({
            type: "POST",
            url: "list",
            
        })
        .done(function(data) {
            if (data.status == 0)
                callback(data.albums);
        })
        .fail(function() {
            console.log("fail");
        });
    }
    
    AlbumList = function(listener) {
        this.albums = [];
        this.node = $("#album_list");
        this.listener = listener;
        this.list_node = this.node.find('ul');  
    }
    
    AlbumList.prototype = {
        request: function(callback) {
            request_albums(function(data) {
                callback(data);
            }); 
        }, 
        view: function(idx) {
            if (0 > idx) return;
            if (idx >= this.albums.length) return;
            
            this.node.find('button').text(this.albums[idx].name);
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
            });
            
            that.albums.push({id: album_id, name: name});
            that.list_node.append(node);
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
    
});