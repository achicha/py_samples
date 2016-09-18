'use strict';
angular.module('todoListApp')
    .controller('mainCtrl', function ($scope, dataService) {
        $scope.helloConsole = dataService.helloConsole;

        $scope.addTodo = function () {
            var todo = {name: "This is a new todo."};
            //add element to the end of todos scope by push
            //$scope.todos.push(todo);
            //add to the beginning
            $scope.todos.unshift(todo)
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