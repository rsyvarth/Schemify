describe('StoryService', function () {

    var ob = karmaHelpers.setup('service', 'StoryService');

    it('should have all dependencies', function () {
        var service = create(); 
        expect(service.$http).to.be.an('function');
        expect(service.$q).to.be.a('function');
    });

    it('should have a getStories method which returns a promise', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('GET', /.+\/palettes/)
                .respond(data);

            $httpBackend.expectGET(/.+\/palettes/);
            back = $httpBackend;
        });

        expect(service.getStories).to.exist;

        var res = service.getStories();
        expect(res).to.exist;
        expect(res.then).to.exist;

        back.flush();

        res.then(function(data){
            expect(data).to.equal(data);
        });
    });

    it('getStories should accept cursors and filters', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('GET', /.+\/palettes?cursor=123&user_id=1/)
                .respond(data);

            $httpBackend.expectGET(/.+\/palettes?cursor=123&user_id=1/);
            back = $httpBackend;
        });

        var res = service.getStories(123, {user_id: 1});
        back.flush();

        res.then(function(data){
            expect(data).to.equal(data);
        });
    });

    it('should have a getStory method which returns a promise', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('GET', /.+\/palettes\/1/)
                .respond(data);

            $httpBackend.expectGET(/.+\/palettes\/1/);
            back = $httpBackend;
        });

        expect(service.getStory).to.exist;

        var res = service.getStory(1);
        expect(res).to.exist;
        expect(res.then).to.exist;

        back.flush();

        res.then(function(data){
            expect(data).to.equal(data);
        });
    });

    it('should have an add method which returns a promise', function () {
        var back;
        var data = {data: ['1','2']};
        var service = create(function($httpBackend){
            $httpBackend.when('POST', /.+\/palettes/)
                .respond(data);

            $httpBackend.expectPOST(/.+\/palettes/);
            back = $httpBackend;
        });

        expect(service.getStory).to.exist;

        var res = service.add(data);
        expect(res).to.exist;
        expect(res.then).to.exist;

        back.flush();

        res.then(function(data){
            expect(data).to.equal(data);
        });
    });

});
