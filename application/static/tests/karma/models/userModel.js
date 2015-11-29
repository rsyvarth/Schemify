describe('UserModel', function () {

	karmaHelpers.setup('model', 'UserModel');

    it('should have all dependencies', function () {
        var model = create(); 
        expect(model.events).to.be.an('object');
        expect(model.$q).to.be.a('function');
        expect(model.userService).to.be.a('object');
    });

    it('should have a loadSelf method which returns a promise', function () {
        var model = create(); 
        sinon.stub(model.userService, 'getSelf', function(){ 
            var deferred = this.$q.defer();
            deferred.resolve([1,2]);
            return deferred.promise;
        });

        var res = model.loadSelf();

        model.userService.getSelf.should.have.been.calledOnce;

        res.then(function(){
            expect(model.user).to.be.deep.equal([1,2]);
        });
    });

    it('should have a subscribe method which returns a promise', function () {
        var model = create(); 
        sinon.stub(model.userService, 'updateSelf', function(data){ 
            var deferred = this.$q.defer();
            deferred.resolve(data);
            return deferred.promise;
        });

        var res = model.subscribe(1);

        model.userService.updateSelf.should.have.been.calledOnce;

        res.then(function(){
            expect(model.user).to.be.deep.equal({subscribed: 1});
        });
    });


    it('should have a getSelf method which returns a user', function () {
        var model = create(); 
        model.user = [1,2];

        var res = model.getSelf();

        expect(res).to.be.deep.equal([1,2]);
    });

});
