angular.module("todoListApp", [])

    .controller('mainCtrl', function ($scope) {
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

    });


