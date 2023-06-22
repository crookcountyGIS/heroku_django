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

        let basemapToggle = new BasemapToggle({
            view: view,  
            nextBasemap: "hybrid"  
          });
    
          // add basemap toggle
          view.ui.add(basemapToggle, "top-left");

          // return home button
        let homeWidget = new Home({
            view: view
          });
          
          // adds the home widget to the top left corner of the MapView
          view.ui.add(homeWidget, "top-left");

        let legend = new Legend({
            view: view,
            container: "legend"
        });
        
        // create renderder for subdivisions
        const subdivisionRenderer = {
            type: "simple", 
            symbol: {
                type: "simple-fill", 
                style: "none",
                outline: {
                    color: [165, 19, 200, 1]
                },
                color: [245, 208, 253, 0.5]
            },
            label: "Subdivisions"
        };

        // create renderer for taxlots 
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

        const fLayer = new FeatureLayer ({
            url: "http://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/1"
        });

        const fLayer2 = new FeatureLayer ({
            url: "http://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/2"
        });




        // add feature from MapServer
        const landGroup = new MapImageLayer({
            url: "https://geo.co.crook.or.us/server/rest/services/publicApp/landGroup/MapServer",
            sublayers: [{
                    id: 0,
                    renderer: subdivisionRenderer,
                    visible: false,
                    popupTemplate: {
                        title: "Subdivision: {name}"
                    },

                },
                {
                    id: 1,
                    renderer: taxlotRenderer,
                    visible: true,
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
                    visible: true,
                    opacity: 0.5
                }
            ]
        });

        const districtsGroup = new MapImageLayer({
            url: "https://geo.co.crook.or.us/server/rest/services/publicApp/districtsGroup/MapServer",
            sublayers: [{
                    id: 12,
                    visible: true,
                    opacity: 0.6
                }, 
                {
                    id: 0,
                    visible: false
                }, 
                {
                    id: 1,
                    visible: true
                }, 
                {
                    id: 2,
                    visible: true
                }, 
                {
                    id: 3,
                    visible: true
                },
                {
                    id: 4,
                    visible: true
                },
                {
                    id: 5,
                    visible: true
                },
                {
                    id: 6,
                    visible: true
                },
                {
                    id: 7,
                    visible: true
                },
                {
                    id: 8,
                    visible: true
                },
                {
                    id: 9,
                    visible: true
                },
                {
                    id: 10,
                    visible: true
                },
                {
                    id: 11,
                    visible: true
                }
            ],
        });



        // add table to query based on selections
        const prop = new FeatureLayer({
            url: "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0",
            //outFields: ["*"]
        });

        // load layers
        view.when(() => {
            console.log("im in paaaatsssssss")
            console.log(window.location.href);
            map.add(fLayer);
            map.add(fLayer2);
            map.add(landGroup);
            map.add(districtsGroup);
            map.add(prop);

        });

        districtsGroup.when(() => {

            districtsGroup.visible = false;
            var checkBoxDistrictsLayer = document.getElementById("districtsLayer");

            checkBoxDistrictsLayer.addEventListener("change", function(e) {
                districtsGroup.visible = e.target.checked;
            });
        });

        const subdivisions = landGroup.sublayers.getItemAt(0);
        const mtLayer = landGroup.sublayers.getItemAt(1);
        const pendingLayer = landGroup.sublayers.getItemAt(6);

        landGroup.when(() => {

            var checkBoxLandGroup = document.getElementById("checkBoxLayer");
            var checkBoxSubdivision = document.getElementById("subdivisions");
            var checkBoxTaxlots = document.getElementById("taxlots");
            var checkBoxPendingLayer = document.getElementById("pendingLayer");


            checkBoxLandGroup.addEventListener("change", function(e) {
                landGroup.visible = e.target.checked;
            });

            checkBoxSubdivision.addEventListener("change", function(e) {
                subdivisions.visible = e.target.checked;
            });

            checkBoxTaxlots.addEventListener("change", function(e) {
                mtLayer.visible = e.target.checked;
            });

            checkBoxPendingLayer.addEventListener("change", function(e) {
                pendingLayer.visible = e.target.checked;
            });


        });

        // query the Property table
        function queryPropTable(results) {
            for ([key, value] of Object.entries(results.features[0].attributes)) {
                //console.log(`${key}: ${value}`);
                if (`${key}` == 'ACCOUNT') {
                    tableWhere = "account_id = '" + `${value}` + "'"

                    const tableQuery = new Query({
                        where: tableWhere,
                        returnGeometry: false,
                        outFields: ["*"]
                    });

                    prop.when(function() {
                        return prop.queryFeatures(tableQuery);
                    }).then(propResults)
                }
            }
        }

        // when a tax lot is clicked, send the query to the queryPropTable function
        view.on("click", function(evt) {

            var query = new Query();
            query.geometry = evt.mapPoint;

            query.outFields = ["*"];
            query.returnGeometry = true;
            query.spatialRelationship = "intersects";
            mtLayer.queryFeatures(query).then(function(results) {

                queryPropTable(results);

            });
        });


        // create search widget with search options
        const searchWidget = new Search({
            view: view,
            container: "searchWidget",
            allPlaceholder: "Maptaxlot, Account, Situs Address, or Owner Name",
            includeDefaultSources: false,
            sources: [{
                    layer: mtLayer,
                    searchFields: ["MAPTAXLOT"],
                    suggestionTemplate: "{MAPTAXLOT}",
                    //displayField: "MAPTAXLTOT",
                    exactMatch: false,
                    outFields: ["*"],
                    name: "Maptaxlot",
                    placeholder: "Search Map Taxlot...",
                },
                {
                    layer: mtLayer,
                    searchFields: ["ACCOUNT"],
                    suggestionTemplate: "{ACCOUNT}",
                    exactMatch: false,
                    outFields: ["*"],
                    //placeholder: "Account: Casey",
                    name: "Account ID",
                    placeholder: "Search by Account #...",
                    //zoomScale: 500000,
                },
                {
                    layer: mtLayer,
                    searchFields: ["SITUS_ADDRESS"],
                    suggestionTemplate: "{SITUS_ADDRESS}",
                    exactMatch: false,
                    outFields: ["*"],
                    //placeholder: "Account: Casey",
                    name: "Situs Address",
                    placeholder: "Search Situs Address...",
                    //zoomScale: 500000,
                },
                {
                    layer: mtLayer,
                    searchFields: ["OWNER_NAME"],
                    suggestionTemplate: "{OWNER_NAME}",
                    exactMatch: false,
                    outFields: ["*"],
                    //placeholder: "Account: Casey",
                    name: "Owner Name",
                    placeholder: "e.g., SMITH JOHN",
                    //zoomScale: 500000,
                },

            ]
        });



        searchWidget.on("select-result", function(event) {
            populateTables(event);
        });


        function populateTables(event) {

            if (event) {
                for ([key, value] of Object.entries(event.result)) {
                    //console.log(`${key}: ${value}`);

                    if (`${key}` == 'name') {
                        const maptaxlot = `${value}`

                        mt_whereClause = "MAPTAXLOT = '" + maptaxlot + "'";

                        const mtQuery = new Query({
                            where: mt_whereClause,
                            returnGeometry: true,
                            outFields: ["*"]
                        });

                        mtLayer.queryFeatures(mtQuery).then(function(mtResults) {

                            if (mtResults.features.length > 0) {
                                queryPropTable(mtResults);
                            }

                        });
                    }
                }
            }
        }



        function propResults(results) {

            // account information
            document.getElementById("owner-name").innerText = results.features[0].attributes.owner_name;
            document.getElementById("map-tax-lot").innerText = results.features[0].attributes.map_taxlot;
            document.getElementById("situs-address").innerText = results.features[0].attributes.situs_address;
            document.getElementById("tax-status").innerText = results.features[0].attributes.tax_status;

            // real market values
            const land = parseInt(results.features[0].attributes.rmv_land);
            const land_num = land.toLocaleString('en-US');
            document.getElementById("land").innerText = '$' + land_num;
            const improv = parseInt(results.features[0].attributes.rmv_improvements);
            const improv_num = improv.toLocaleString('en-US');
            document.getElementById("structures").innerText = '$' + improv_num;
            const rmv_total = results.features[0].attributes.rmv_total;
            const rmv_total_num = rmv_total.toLocaleString('en-US');
            document.getElementById("total").innerText = '$' + rmv_total_num;

            // assessed values
            const spec = parseInt(results.features[0].attributes.maximum_av);
            const spec_num = spec.toLocaleString('en-US');
            document.getElementById("specially_assessed").innerText = '$' + spec_num;
            const tax_av = results.features[0].attributes.taxable_av;
            const tax_av_num = tax_av.toLocaleString('en-US');
            document.getElementById("assessed_value").innerText = '$' + tax_av_num;
            const vet = results.features[0].attributes.veterans_exemption;
            const vet_num = vet.toLocaleString('en-US');
            document.getElementById("vet_exception").innerText = '$' + vet_num;

        }

    });