'use strict';

var LikeButtonDirective = BaseDirective.extend({
  userModel: null,

  /**
   * Init Class
   */
  init: function($scope, Events, LikeModel) {
    this.likeModel = LikeModel;
    this._super($scope, Events);
  },

  /**
   * Add event listener for USER_LOADED which is fired when the
   * StoryModel has a new set of stories.
   */
  addListeners: function() {
    this._super();

    this.likeUpdated = this.likeUpdated.bind(this);
    this.events.addEventListener(models.events.LIKE_UPDATED, this.likeUpdated);
  },

  /**
   * Setup scope
   */
  setupScope: function() {
    this.$scope.story.liked = !!this.$scope.story.user_like;
    this.$scope.story.toggleLike = this.toggleLike.bind(this);
  },

  /**
   * Unbind event listeners on class destroy
   */
  destroy: function() {
    this._super();
    this.events.removeEventListener(models.events.LIKE_UPDATED, this.likeUpdated);
  },

  likeUpdated: function(event, palette_id, like) {
    if(this.$scope.story.id == palette_id) {
      if(like && like.id) {
        this.$scope.story.like_count++;
        this.$scope.story.user_like = like;
      } else {
        this.$scope.story.like_count--;
        this.$scope.story.user_like = false;
      }
      this.$scope.story.liked = !!this.$scope.story.user_like;
    }
  },

  toggleLike: function() {
    if(this.$scope.story.liked) {
      this.likeModel.remove(this.$scope.story.id);
    } else {
      this.likeModel.add(this.$scope.story.id);
    }
  }

});

angular.module('likeButton',[])
  .directive('likeButton', function(Events, LikeModel) {
  return {
    restrict: 'E',
    isolate: false,
    link: function($scope) {
      new LikeButtonDirective($scope, Events, LikeModel);
    },
    scope: {
      story: '='
    }
  };
});
