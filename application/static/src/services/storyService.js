'use strict';

var StoryService = Class.extend({
  $q: null,
  $http: null,
  baseUrl: config.baseUrl + 'api',

  /**
   * Init class
   */
  init: function($q, $http) {
    this.$q = $q;
    this.$http = $http;
  },

  /**
   * Pull a list of the latest stories
   */
  getStories: function(cursor, filters) {
    var deferred = this.$q.defer();

    var params = filters ? filters : {};
    if(cursor) {
      params.cursor = cursor;
    }

    this.$http({
      method: 'GET',
      url: this.baseUrl + '/palettes',
      params: params
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  },

  /**
   * Pull a list of the latest stories
   */
  getStory: function(id) {
    var deferred = this.$q.defer();

    this.$http({
      method: 'GET',
      url: this.baseUrl + '/palettes/' + id
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  },

  add: function(data) {
    var deferred = this.$q.defer();

    this.$http({
      method: 'POST',
      url: this.baseUrl + '/palettes',
      data: data
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  }

});

(function() {
  var StoryServiceProvider = Class.extend({
    $get: function($q, $http) {
      return new StoryService($q, $http);
    }
  });

  angular.module('story.StoryService',[])
    .provider('StoryService', StoryServiceProvider);
}());
