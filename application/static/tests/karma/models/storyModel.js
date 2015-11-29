describe('StoryModel', function () {

	karmaHelpers.setup('model', 'StoryModel');

    it('should have all dependencies', function () {
        var model = create(); 
        expect(model.events).to.be.an('object');
        expect(model.$q).to.be.a('function');
        expect(model.storyService).to.be.a('object');
    });

    it('should have a loadStories method which returns a promise', function () {
        var model = create(); 
        sinon.stub(model.storyService, 'getStories', function(){ 
            var deferred = this.$q.defer();
            deferred.resolve([1,2]);
            return deferred.promise;
        });

        var res = model.loadStories();

        model.storyService.getStories.should.have.been.calledOnce;

        res.then(function(){
            expect(model.stories).to.be.deep.equal([1,2]);
        });
    });

    it('should have a loadStory method which returns a promise', function () {
        var model = create(); 
        sinon.stub(model.storyService, 'getStory', function(id){ 
            var deferred = this.$q.defer();
            deferred.resolve([id,2]);
            return deferred.promise;
        });

        var res = model.loadStory(1);

        model.storyService.getStory.should.have.been.calledOnce;

        res.then(function(){
            expect(model.story[0]).to.be.equal(1);
            expect(model.story[1]).to.be.equal(2);
            expect(model.story['timestamp']).to.exist;
        });
    });


    it('should have a getStories method which returns a stories', function () {
        var model = create(); 
        model.stories = [1,2];

        var res = model.getStories();

        expect(res).to.be.deep.equal([1,2]);
    });


    it('should have a getStory method which returns a story', function () {
        var model = create(); 
        model.story = [1,2];

        var res = model.getStory();

        expect(res).to.be.deep.equal([1,2]);
    });


    it('should have a add method which returns a promise', function () {
        var model = create(); 
        sinon.stub(model.storyService, 'add', function(data){ 
            var deferred = this.$q.defer();
            deferred.resolve(data);
            return deferred.promise;
        });

        var res = model.add({test: 1});

        model.storyService.add.should.have.been.calledOnce;

        res.then(function(){
            expect(model.story).to.be.deep.equal({test: 1});
        });
    });


});
