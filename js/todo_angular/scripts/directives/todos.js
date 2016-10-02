angular.module('todoListApp')
    .directive('todos', function () {
        return {
            templateUrl: 'templates/todos.html',
            controller: 'mainCtrl',
            replace: true // remove our custom todos tags from html
        }
    })