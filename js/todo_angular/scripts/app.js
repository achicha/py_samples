angular.module("todoListApp", [])

    .controller('mainCtrl', function ($scope, dataService) {
        $scope.helloConsole = dataService.helloConsole;

        $scope.helloWorld = function () {
            console.log("Hello there! This is helloWorld controller function, in the main Ctrl!");
        };
        dataService.getTodos(function (response) {
                    console.log(response.data);
                    $scope.todos = response.data;
                });
    })

    .service('dataService', function ($http) {
        this.helloConsole = function () {
            console.log("This is the hello console service!");
        };
        this.getTodos = function(callback) {
            $http.get('mock/todos.json')
                .then(callback)
        }
    });


