'use strict';

var LikeService = Class.extend({
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

  add: function(palette_id) {
    var deferred = this.$q.defer();
    var data = {
      palette_id: palette_id
    };

    this.$http({
      method: 'POST',
      data: data,
      url: this.baseUrl + '/likes'
    }).then(function(data) {
      deferred.resolve(data.data);
    }, function(err) {
      console.error(err); //TODO: real error handling
      deferred.reject(err);
    });

    return deferred.promise;
  },

  remove: function(palette_id) {
    var deferred = this.$q.defer();

    this.$http({
      method: 'DELETE',
      url: this.baseUrl + '/likes?palette_id='+palette_id
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
  var LikeServiceProvider = Class.extend({
    $get: function($q, $http) {
      return new LikeService($q, $http);
    }
  });

  angular.module('like.LikeService',[])
    .provider('LikeService', LikeServiceProvider);
}());
