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
                        'video_url': 'https://d11rse4z1ry9t6.cloudfront.net/12da932b-cfd1-4208-ab9d-e05d7140bc3c/AppleHLS1/Fireaway_Pizza_Trim.m3u8',
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