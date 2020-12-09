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
                        'video_url': 'https://www.youtube.com/watch?v=SGyVUNUnUQk',
                        'title': 'Clip title',
                        'description': 'lorem ipsum dolem amet #food #seafood'
                    },
                    {
                        'id': 2,
                        'thumbnail_url': '',
                        'video_url': 'https://www.youtube.com/watch?v=SGyVUNUnUQk',
                        'title': 'Another clip',
                        'description': 'describing the food #breakfast #morningroll #bacon'
                    },
                    {
                        'id': 3,
                        'thumbnail_url': '',
                        'video_url': 'https://www.youtube.com/watch?v=SGyVUNUnUQk',
                        'title': 'Third clip',
                        'description': 'description here #sushi #asian'
                    }
                ]
            }
        ]