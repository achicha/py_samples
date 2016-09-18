angular.module("todoListApp", [])

    .controller('mainCtrl', function ($scope, dataService) {
        $scope.helloConsole = dataService.helloConsole;

        $scope.helloWorld = function () {
            console.log("Hello there! This is helloWorld controller function, in the main Ctrl!");
        };

    $scope.todos = [
        {"name": "first"},
        {"name": "second"},
        {"name": "third"},
        {"name": "four"},
        {"name": "five"},
        {"name": "six"}
    ]

    })

    .service('dataService', function () {
        this.helloConsole = function () {
            console.log("This is the hello console service!");
        }
    });


