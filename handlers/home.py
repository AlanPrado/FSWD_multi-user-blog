import json
from common.database import Post
from common.request import BlogHandler, Page

class WelcomeHandler(BlogHandler):
    def render_post_form(self, error="", content="", subject=""):
        self.render('post_form.html', page=self, error=error, subject=subject, content=content)

    def get_page_stack(self):
        return [Page(label='Home', url='/blog')]

    def get(self):
        if self.is_user_authenticated():
            posts = Post.get_most_recent()
            self.render('welcome.html', page=self, posts=posts)

    def is_owner(self, post):
        return post.author.key().id() == self.user.key().id()

class NewPostHandler(WelcomeHandler):
    def get_page_stack(self):
        pages = super(NewPostHandler, self).get_page_stack()
        pages.append(Page(label='New Post', url='/blog/newpost'))
        return pages

    def get(self):
        if self.is_user_authenticated():
            self.render_post_form()

    def post(self):
        if self.is_user_authenticated():
            subject = self.request.POST['subject']
            content = self.request.POST['content']

            if subject and content:
                post = Post.register(subject=subject, content=content, author=self.user)
                post_id = post.key().id()
                post_url = "/blog/%s" % post_id
                self.redirect(post_url, permanent=True)
            else:
                error = 'subject and content, please!'
                self.render_post_form(error=error, subject=subject, content=content)

class EditPostHandler(WelcomeHandler):
    def get_page_stack(self):
        pages = super(EditPostHandler, self).get_page_stack()
        pages.append(Page(label='Edit Post', url='/blog/edit/%s' % self.post_id))
        return pages

    def get(self, post_id):
        if self.is_user_authenticated():
            self.post_id = post_id
            post = Post.by_id(int(post_id))

            if not post:
                self.redirect("/blog", permanent=True)
            else:
                self.render_post_form(subject=post.subject, content=post.content)

    def post(self, post_id):
        if self.is_user_authenticated():
            self.post_id = post_id
            subject = self.request.POST['subject']
            content = self.request.POST['content']

            if not post_id and not post_id.isdigit():
                self.redirect("/blog", permanent=True)
            elif not (subject and content):
                error = 'subject and content, please!'
                self.render_post_form(error=error, subject=subject, content=content)
            else:
                self.post_id = post_id
                post = Post.by_id(int(post_id))

                if not self.is_owner(post):
                    error = 'Edit other people posts is not allowed.'
                    self.render_post_form(error=error, subject=subject, content=content)
                else:
                    post.update(subject=subject, content=content)
                    post_url = "/blog/%s" % post_id
                    self.redirect(post_url, permanent=True)

class PostHandler(WelcomeHandler):
    def get_page_stack(self):
        pages = super(PostHandler, self).get_page_stack()
        pages.append(Page(label='Post detail', url='/blog/%s' % self.post_id))
        return pages

    def get(self, post_id):
        if self.is_user_authenticated():
            self.post_id = post_id
            post = Post.by_id(int(post_id))

            if not post:
                self.redirect("/blog", permanent=True)
            else:
                self.render('blog_detail.html', page=self, post=post)

    def delete(self, post_id):
        if self.is_user_authenticated():
            post = Post.by_id(int(post_id))

            if not post:
                self.write(json.dumps({"message": "Post already removed!"}))
            elif not self.is_owner(post):
                self.response.set_status(401)
                self.write("Remove other people posts is not allowed.")
            else:
                post.delete()
                self.write(json.dumps({"message": "Post removed!"}))
