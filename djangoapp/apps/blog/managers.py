from django.db.models import Manager

class PostManager(Manager):
    def get_published(self):
        return self.filter(is_published=True)