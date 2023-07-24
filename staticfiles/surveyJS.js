require(["esri/Map",
        "esri/views/MapView",
        "esri/layers/FeatureLayer",
        "esri/layers/MapImageLayer",
        "esri/widgets/BasemapToggle",
        "esri/widgets/Home",
        "esri/widgets/Legend",
        "esri/rest/support/Query",
        "esri/widgets/Search",
        "esri/widgets/Legend",

    ],

    (Map,
        MapView,
        FeatureLayer,
        MapImageLayer,
        BasemapToggle,
        Home,
        Legend,
        Query,
        Search) => {


         //create map object
        const map = new Map({
            basemap: "topo-vector"
        });

        var lat = 44.30291;
        var long = -120.84585;

        // create view
        const view = new MapView({
            container: "viewDiv",
            map: map,
            zoom: 13,
            center: [long, lat] // longitude, latitude
        });

        // let basemapToggle = new BasemapToggle({
        //     view: view,
        //     nextBasemap: "hybrid"
        //   });
        //
        //   // add basemap toggle
        //   view.ui.add(basemapToggle, "top-left");

          // return home button
        let homeWidget = new Home({
            view: view
          });

          // adds the home widget to the top left corner of the MapView
          view.ui.add(homeWidget, "top-left");

        // let legend = new Legend({
        //     view: view,
        //     container: "legend"
        // });



        const fLayer = new FeatureLayer ({
            url: ""
        });


        // load layers
        view.when(() => {

        });



    });