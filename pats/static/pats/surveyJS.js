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
            zoom: 11,
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
            url: "https://geo.co.crook.or.us/server/rest/services/surveyor/surveys/MapServer/0",
             popupTemplate: {
                    title: "Survey {cs}",
                    content: "<strong>PDF:</strong> <a href={image}>View</a> <br /> <strong>Prepared For:</strong> {prepared_for} <br /> <strong>Description:</strong> {identification} <br /> <strong>Year:</strong> {rec_y}",
                }
        });

        const taxlotRenderer = {
            type: "simple",
            symbol: {
                type: "simple-fill",
                style: "none",
                outline : {
                    width: 0.5,
                    color: [0, 0, 0, 1]
                },
                color: [0, 0, 0, 0.5]
             },
            label: "Taxlots"
        };

                // add feature from MapServer
        const landGroup = new MapImageLayer({
            url: "https://geo.co.crook.or.us/server/rest/services/publicApp/landGroup/MapServer",
            sublayers: [{
                    id: 0,
                    visible: false,
                },
                {
                    id: 1,
                    renderer: taxlotRenderer,
                    visible: false,
                    popupTemplate: {
                        title: "{MAPTAXLOT}",
                        content: "Owner Name: {OWNER_NAME} <br /> Zone: {ZONE} <br /> Account: {ACCOUNT} <br /> PATS Link: <a href={PATS_LINK}>PATS Link</a> <br /> Tax Map Link: <a href={TAX_MAP_LINK}>Tax Map Link</a> <br /> Tax Card Link: <a href={TAX_CARD_LINK}>Tax Card Link</a>",
                    }
                },
                {
                    id: 3,
                    visible: false
                },
                {
                    id: 4,
                    visible: false
                },
                {
                    id: 5,
                    visible: false
                },
                {
                    id: 6,
                    visible: false,
                    opacity: 0.6
                },
                {
                    id: 7,
                    visible: false,
                    opacity: 0.5
                }
            ]
        });

        const mtLayer = landGroup.sublayers.getItemAt(1);
        console.log(mtLayer);
        // load layers
        view.when(() => {
             map.add(fLayer);
             map.add(landGroup);

        });


        console.log("{{ i|safe }}");



    });