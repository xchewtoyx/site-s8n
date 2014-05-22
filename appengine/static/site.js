var Site = {
    init : function () {
        this.applyStyles();
    },

    applyStyles: function () {
        // Style base document
        $("div.body").addClass("col-sm-8");
        $("div.breadcrumbs").addClass("col-sm-8");
        $("div.related").addClass("col-sm-3 col-sm-offset 1");
        $("div.related ol").addClass("nav nav-pills pull-right");

        // Replace default sphinx permalink mark with right-aligned glyph
        $("a.headerlink").wrap("<span class='pull-right'/>");
        $("a.headerlink").empty().append(
            "<i class='fa fa-fw fa-link'></i>");

        // Style sidebar
        $("div.sidebar").addClass("col-sm-3 col-sm-offset-1");
        $("div.sidebar>.panel").addClass("panel-default");
        $("div.sidebar div.heading").addClass("panel-heading");
        $("div.sidebar div.content").addClass("panel-body");
        $("div.panel-heading").addClass("lead");
        $("div.panel-body ul").addClass("nav nav-pills nav-stacked");

        // Style logo panel
        $("div.logo").addClass('well');
        $("p.logo").addClass('text-center');
        $("div.g-plusone,div.fb-like").wrap("<div class='social'></div>");

        // Style bio panel
        $("div.bio").addClass('panel panel-default');
        $("div.bio > .heading").addClass('panel-heading lead');
        $("div.bio > .heading").nextAll().wrapAll(
            "<div class='panel-body'></div>");
        $("div.bio div.btn-group").wrap("<div class='text-center'></div>");
        $("div.bio i.fa").addClass("fa-fw");

        // Style admonitions
        $(".admonition").addClass("alert");
        $(".admonition-title").addClass("lead");
        $(".admonition a").addClass("alert-link");
        $(".admonition").filter( ".note" ).addClass("alert-info");
        $(".admonition").filter( ".warning" ).addClass("alert-warning");

        // Enable tooltips
        $("a.headerlink").attr('data-toggle', 'tooltip');
        $("a.headerlink").attr('data-placement', 'left');
        $("[data-toggle='tooltip']").tooltip();

        // Style carousels
        var carousels = $( "div.carousel" );
        carousels.addClass("ui-widget-content");
        for( var i = 0; i < carousels.length; i++ ) {
            $(carousels[i]).attr("id", "carousel-id-"+i);
            this.addCarousel.apply(carousels[i]);
        }

        // Style images
        $( "img.center" ).wrap("<div class='text-center'></div>");
        $("div.body img").addClass("img-responsive");

        // Style tables
        $("table.docutils").not(".table").addClass("table table-striped");
    },

    addCarousel: function () {
        var uniqueid = $(this).attr("id");
        var images = $( this ).find(">img, .figure");
        var active;

        // Fixup the base div
        $( this ).removeClass("container");
        $( this ).addClass("slide");
        $( this ).attr("data-ride", "carousel");

        // Add indicators
        $( this ).append("<ol class='carousel-indicators' />");
        var indicators = $( this ).find("ol.carousel-indicators");
        for (var i = 0; i < images.length; i++) {
            $( indicators ).append(
                "<li data-target='#"+this.id+"' data-slide-to='" +
                    i + "'></li>"
            );
        }

        // Wrap images and captions appropriately
        images.wrapAll("<div class='carousel-inner'></div>");
        images.wrap("<div class='item'><div class='inner'></div></div>");
        images.find(".caption").addClass("carousel-caption");

        // Set the initial active indicator and image
        active = $( indicators ).find('li')[0];
        $( active ).addClass("active");
        active = $( this ).find("div.item")[0];
        $( active ).addClass("active");

        // Align images in the center when they don't fill the width
        $( this ).find("div.inner").addClass("text-center");

        // Add the controls
        $( this ).append(
            "<a class='left carousel-control' href='#" + this.id +
                "' data-slide='prev'></a>");
        $( this ).find("a.left").append(
            "<span class='glyphicon glyphicon-chevron-left'></span>");
        $( this ).append(
            "<a class='right carousel-control' href='#" + uniqueid +
                "' data-slide='next'></a>");
        $( this ).find("a.right").append(
            "<span class='glyphicon glyphicon-chevron-right'></span>");
    },
};

$(document).ready( function () {
    Site.init();
});
