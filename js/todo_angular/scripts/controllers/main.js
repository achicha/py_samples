'use strict';
angular.module('todoListApp')
    .controller('mainCtrl', function ($scope, dataService) {
        $scope.helloConsole = dataService.helloConsole;

        $scope.addTodo = function () {
            var todo = {name: "This is a new todo."};
            //update todos scope by push
            $scope.todos.push(todo);
        };
        dataService.getTodos(function (response) {
                    console.log(response.data);
                    $scope.todos = response.data;
                });
        $scope.deleteTodo = function (todo, $index) {
            dataService.deleteTodo(todo);
            $scope.todos.splice($index, 1);
        };
        $scope.saveTodo = function (todo) {
            dataService.saveTodo(todo);
        };
    });