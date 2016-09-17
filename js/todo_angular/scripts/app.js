angular.module("todoListApp", [])

    .controller('mainCtrl', function ($scope) {
        $scope.helloWorld = function () {
            console.log("Hello there! This is helloWorld controller function, in the main Ctrl!");
        };
    })

    .controller('coolCtrl', function ($scope) {
        $scope.whoAmI = function () {
            console.log("hello there, this is the coolCtrl function!");
        };

        $scope.helloWorld = function () {
            console.log("this is not main ctrl!");
        };
    });;

