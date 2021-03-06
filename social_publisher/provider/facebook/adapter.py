#coding=utf-8
import logging
from allauth.socialaccount.models import SocialToken, SocialApp
from facebook import GraphAPI
from social_publisher.provider import MessageProvider, ImageProvider, VideoProvider, registry

logger = logging.getLogger(__name__)


class FacebookAdapter(MessageProvider, ImageProvider, VideoProvider):
    id = 'facebook'
    name = 'FacebookAdapter'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.social_token = SocialToken.objects.filter(app__provider='facebook',
                                                       account__provider='facebook',
                                                       account__user=user)
        self.facebook = GraphAPI(self.social_token.get().token)
        self.social_app = SocialApp.objects.filter(id=self.social_token.get().app.id)

    def publish_image(self, image, message='', **kwargs):
        try:
            logger.info('trying to update facebook status with an image, for user: %s' % self.user)
            result = self.facebook.put_photo(open(image.path), message, **kwargs)
            logger.info(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e

    def publish_message(self, message, **kwargs):
        try:
            logger.info('trying to update facebook status, for user: %s' % self.user)
            result = self.facebook.put_wall_post(message)
            logger.info(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e

    def publish_video(self, video, title='', description='', **kwargs):
        try:
            logger.info('trying to update facebook status with a video, for user: %s' % self.user)
            result = self.facebook.put_video(open(video.path), title=title, description=description)
            logger.info(str(result))
            return result
        except Exception as e:
            logger.error(e)
            raise e


registry.register(FacebookAdapter)