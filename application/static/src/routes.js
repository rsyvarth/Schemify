'use strict';

app.config(function($stateProvider, $urlRouterProvider) {

  // For any unmatched url, redirect to /
  $urlRouterProvider.otherwise('/');

  // Now set up the states
  $stateProvider
    .state('about', {
      url: '/about',
      templateUrl: 'partials/about/about.html'
    })
    .state('create', {
      url: '/create',
      templateUrl: 'partials/create/create.html'
    })
    .state('view', {
      url: '/post/:postId',
      templateUrl: 'partials/view/view.html',
      controller: ViewController
    })
    .state('profile', {
      url: '/user/:userId/:page',
      params: {
        userId: {value: ''},
        page: {value: '', squash: true}
      },
      templateUrl: 'partials/profile/profile.html',
      controller: ProfileController
    })
    .state('home', {
      url: '/:page',
      params: {
        page: {value: '', squash: true}
      },
      templateUrl: 'partials/home/home.html',
      controller: HomeController
    });
});
