describe('UserService', function () {

	var ob = karmaHelpers.setup('service', 'UserService');

    it('should have all dependencies', function () {
        var service = create(); 
        expect(service.$http).to.be.an('function');
        expect(service.$q).to.be.a('function');
    });

    it('should have a getSelf method which returns a promise', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('GET', /.+\/users\/self/)
                .respond(data);

            $httpBackend.expectGET(/.+\/users\/self/);
            back = $httpBackend;
        });

        expect(service.getSelf).to.exist;

        var res = service.getSelf();
        expect(res).to.exist;
        expect(res.then).to.exist;

        back.flush();

        res.then(function(resp){
            expect(resp).to.deep.equal(data);
        });
    });

    it('should have an updateSelf method which returns a promise', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('PUT', /.+\/users\/self/)
                .respond(data);

            $httpBackend.expectPUT(/.+\/users\/self/);
            back = $httpBackend;
        });

        expect(service.updateSelf).to.exist;

        var res = service.updateSelf(data);
        expect(res).to.exist;
        expect(res.then).to.exist;

        back.flush();

        res.then(function(resp){
            expect(resp).to.deep.equal(data);
        });
    });

});
