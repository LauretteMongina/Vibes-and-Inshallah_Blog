import unittest
from app.models import Blog_post, User,
from app import db


class BlogModelTest(unittest.TestCase):
    def setUp(self):
        self.user_laurah = User(username='laurah', password='dddd', email='test@test.com')
        self.new_blog = Blog_post(id=1, title='Test', content='This is a test blog', user_id=self.user_laurah.id)

    def tearDown(self):
        Blog_post.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog_post.title, 'Test')
        self.assertEquals(self.new_blog_post.content, 'This is a test blog')
        self.assertEquals(self.new_blog_post.user_id, self.user_laurah.id)

    def test_save_blog_post(self):
        self.new_blog_post.save()
        self.assertTrue(len(Blog_post.query.all()) > 0)

    def test_get_blog_post(self):
        self.new_blog_post.save()
        got_blog = Blog_post.get_blog(1)
        self.assertTrue(get_blog_post is not None)