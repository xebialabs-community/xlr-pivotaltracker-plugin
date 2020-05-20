/*
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
'use strict';

(function () {

    var pivotaltrackerTileViewController = function($scope, ptService, XlrTileHelper) {
        
        var vm = this;

        vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;

        vm.storiesSummaryData = {
            count: 0,
            types: []
        };

        vm.stories=[];
        
        vm.colors = {};
        vm.colors.feature = '#ffd025';
        vm.colors.bug = '#009cd8';
        vm.colors.release = '#991C71';
        vm.colors.chore = '#008771';

        vm.chartOptions = {
            topTitleText: function(data){
                return data.count;
            },
            bottomTitleText: function(data){
                if(data.count > 1){
                    return "stories";
                } else {
                    return "story";
                }
            },
            series: function (data) {
                var result= [];
                data.types.forEach(function(item, index, array){
                    result.push({
                        y: item.count,
                        name: item.type,
                        color: vm.colors[item.type]
                    })
                });
                return [{ data: result }]; 
                },
            showLegend: false,
            donutThickness: '60%'
        };

        vm.gridOptions = {
            enableFiltering: false,
            columnDefs:[{ 
                field: 'id',
                displayName: 'ID',
                cellTemplate: '<div><a ng-href="{{row.entity.url}}">{{row.entity.id}}</a></div>',
                enableColumnMenu: false
            },{ 
                field: 'name',
                displayName: 'Name',
                enableColumnMenu: false
            },{ 
                field: 'story_type',
                displayName: 'Type',
                enableColumnMenu: false
            },{ 
                field: 'current_state',
                displayName: 'Current State',
                enableColumnMenu: false
            }],
            data: []
        };
    
        function tileConfigurationIsPopulated() {
            const config = vm.tile.properties;
            if (!_.isEmpty(config.stories.variable) && !_.isEmpty(config.pivotaltrackerServer) && !_.isEmpty(config.project_id)) {
                return true;
            }
            if (!_.isEmpty(config.stories.value) && !_.isEmpty(config.pivotaltrackerServer) && !_.isEmpty(config.project_id)) {
                return true;
            }
            return false;
        }
        
        function refresh() {
            load({params: {refresh: true}});
        }
        
        function load(config) {
            if (vm.tileConfigurationIsPopulated()) {
                vm.loading = true;
                ptService.executeQuery(vm.tile.id, config).then(
                    function(response) {
                        mapResponseToUi(response);
                    })
                    .finally(
                        function() {
                            vm.loading = false;
                    });
            }
        }
        
        function mapResponseToUi(response) {
            var data = response.data.data;
            vm.stories = data.stories;

            vm.storiesSummaryData = {
                count: data.count,
                types: data.types,
            };

            vm.storiesSummaryData.types.forEach(function(value, index) {
                vm.storiesSummaryData.types[index].color = vm.colors[value.type];
            });

            vm.stories.forEach(function(story, index){
                vm.gridOptions.data[index] = {
                    id: story['id'],
                    name: story['name'],
                    story_type: story['story_type'],
                    current_state: story['current_state'],
                    url: story['url']
                };
            });

        }
        
        vm.$onInit = function () {
            if ($scope.xlrDashboard) {
                // summary page
                vm.release = $scope.xlrDashboard.release;
                vm.tile = $scope.xlrTile.tile;
                if (vm.tile.properties == null) {
                    vm.config = vm.tile.configurationProperties;
                } else {
                    // new style since 7.0
                    vm.config = vm.tile.properties;
                }
            } else {
                // detail page
                vm.release = $scope.xlrTileDetailsCtrl.release;
                vm.tile = $scope.xlrTileDetailsCtrl.tile;
            }
            load();
        };
        vm.refresh = refresh;

    };
    
    var pivotaltrackerService = function(Backend) {
        function executeQuery(tileId, config) {
            return Backend.get("tiles/" + tileId + "/data", config);
        }
        return   {
            executeQuery : executeQuery
        };
    }
    
    pivotaltrackerService.$inject = ['Backend'];
    pivotaltrackerTileViewController.$inject = ['$scope', 'xlrelease.pivotaltracker.pivotaltrackerService', 'XlrTileHelper'];
    
    angular.module('xlrelease.pivotaltracker.tile', [])
        .service('xlrelease.pivotaltracker.pivotaltrackerService', pivotaltrackerService)
        .controller('pivotaltracker.TileViewController', pivotaltrackerTileViewController);
    
})();
