from flask_restful import Resource


class Restaurants(Resource):
    @classmethod
    def get(cls):
        return [
            { 
                'id': 1, 
                'name': 'Restaurant name',
                'description': 'about here',
                'clips': [
                    {
                        'id': 1,
                        'thumbnail_url': '',
                        'video_url': 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
                        'title': 'Clip title',
                        'description': 'lorem ipsum dolem amet #food #seafood'
                    },
                    {
                        'id': 2,
                        'thumbnail_url': '',
                        'video_url': 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
                        'title': 'Another clip',
                        'description': 'describing the food #breakfast #morningroll #bacon'
                    },
                    {
                        'id': 3,
                        'thumbnail_url': '',
                        'video_url': 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
                        'title': 'Third clip',
                        'description': 'description here #sushi #asian'
                    }
                ]
            }
        ]