'use strict';

var CreateFormDirective = BaseDirective.extend({
  storyModel: null,
  $state: null,

  /**
   * Init Class
   */
  init: function($scope, Events, StoryModel, $state) {
    this.storyModel = StoryModel;
    this.$state = $state;

    this._super($scope, Events);
    componentHandler.upgradeAllRegistered();
  },

  /**
   * Add event listener for ENTRY_CREATED which is fired when the
   * StoryModel has a new set of stories.
   */
  addListeners: function() {
    this._super();

    this.entryAdded = this.entryAdded.bind(this);
    this.events.addEventListener(models.events.ENTRY_CREATED, this.entryAdded);
  },

  /**
   * Setup scope
   */
  setupScope: function() {
    this.$scope.form = {title: '', description: ''};
    this.$scope.loading = false;

    this.$scope.create = this.create.bind(this);
    this.$scope.uploadComplete = this.uploadComplete.bind(this);
  },

  /**
   * Unbind event listeners on class destroy
   */
  destroy: function() {
    this._super();
    this.events.removeEventListener(models.events.ENTRY_CREATED, this.entryAdded);
  },

  create: function() {
    console.log(this.$scope.form);
    
    //Simple error handling
    if(!this.image) {
      alert("Image is required!");
      return;
    }

    this.$scope.loading = true;
    this.$scope.form.image_id = this.image.id;
    this.storyModel.add(this.$scope.form);
  },

  uploadComplete: function(data) {
    console.log(data);

    //Simple error handling
    if(data.data.message) {
      alert(data.data.message);
      return;
    }

    this.image = data.data;
    this.$scope.imageUrl = config.baseUrl + 'api/images/' + this.image.id;
  },

  entryAdded: function(event, entry) {
    console.log('added', entry);
    this.$state.transitionTo('home');
  }

});

angular.module('createForm',[])
  .directive('createForm', function(Events, StoryModel, $state) {
  return {
    restrict: 'E',
    isolate: true,
    link: function($scope) {
      new CreateFormDirective($scope, Events, StoryModel, $state);
    },
    scope: true,
    templateUrl: 'partials/create/createForm.html'
  };
});
