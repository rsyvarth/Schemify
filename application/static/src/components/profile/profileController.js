'use strict';

/**
 * Profile Controller
 *
 * Manages the home page and controls loading data for the
 * the story list directive.
 */
var ProfileController = Class.extend({
  $scope: null,
  events: null,
  storyModel: null,
  $stateParams: null,

  /**
   * Init class
   */
  init: function($scope, Events, StoryModel, $stateParams) {
    this.$scope = $scope;
    this.events = Events;
    this.storyModel = StoryModel;
    this.$stateParams = $stateParams;

    this.setupScope();
  },

  /**
   * Sets up values on the scope then call the story model to load
   * a list of stories for the current page. (The StoryList directive
   * listens for changes to the story model and will automatically update
   * when the changes are loaded)
   */
  setupScope: function() {
    this.$scope.currPage = this.$stateParams.page;
    this.$scope.userId = this.$stateParams.userId;

    this.storyModel.loadStories(this.$scope.currPage, {user_id: this.$scope.userId});

    this.storiesLoaded = this.storiesLoaded.bind(this);
    this.events.addEventListener(models.events.ENTRIES_LOADED, this.storiesLoaded);
  },

  storiesLoaded: function() {
    var data = this.storyModel.getStories();
    this.$scope.meta = data.meta;
  }

});

ProfileController.$inject = ['$scope', 'Events', 'StoryModel', '$stateParams'];
