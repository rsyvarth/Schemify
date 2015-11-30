'use strict';

/**
 * Define the LIKE_UPDATED event which this model emits
 */
namespace('models.events').LIKE_UPDATED = 'UserModel.LIKE_UPDATED';

/**
 * User Model
 *
 * Pulls most popular user plus scrapes each user's target
 * url in order to retrieve embed information.
 */
var LikeModel = Class.extend({
  events: null,
  $q: null,
  likeService: null,

  /**
   * Init class
   */
  init: function(Events, $q, LikeService) {
    this.events = Events;
    this.$q = $q;
    this.likeService = LikeService;
  },

  add: function(palette_id) {
    var deferred = this.$q.defer();

    this.likeService.add(palette_id).then(function(data) {
      this.events.notify(models.events.LIKE_UPDATED, palette_id, data);
      deferred.resolve(data);
    }.bind(this));

    return deferred.promise;
  },

  remove: function(palette_id) {
    var deferred = this.$q.defer();

    this.likeService.remove(palette_id).then(function(data) {
      this.events.notify(models.events.LIKE_UPDATED, palette_id, data);
      deferred.resolve(data);
    }.bind(this));

    return deferred.promise;
  }
  
});

(function() {
  var LikeModelProvider = Class.extend({
    $get: function(Events, $q, LikeService) {
      return new LikeModel(Events, $q, LikeService);
    }
  });

  angular.module('like.LikeModel',[])
    .provider('LikeModel', LikeModelProvider);
}());
